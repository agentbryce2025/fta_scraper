#!/usr/bin/env python
"""
FTA Scraper - A tool to detect changes to Free Trade Agreements on the Chilean Customs website.
"""

import argparse
import os
import hashlib
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Base URL for Chilean Customs
BASE_URL = "https://www.aduana.cl"
# US FTA specific page
US_FTA_URL = "https://www.aduana.cl/tratado-de-libre-comercio-chile-estados-unidos/aduana/2007-02-28/165004.html"

# Paths to monitor for changes
PATHS_TO_MONITOR = [
    "Reglas de Origen Capítulo 4",
    "Reglas Específicas de Origen Texto Original Anexo 4.1",
    "Enmienda Anexo 4.1 Decreto N° 28 de 2008",
    "Enmienda Anexo 4.1 Decreto N° 117 de 2011",
    "Enmienda Anexo 4.1 Nota S/N de 2011",
    "Enmienda Anexo 4.1 Decreto N° 130 de 2012",
    "Enmienda Anexo 4.1 Decreto N° 17 de 2020",
    "Directrices Comunes - Resolución N° 342 DNA de 20.01.2015"
]

class FTAScraper:
    def __init__(self, output_dir="./data", headless=True):
        self.output_dir = output_dir
        self.headless = headless
        self.data_file = os.path.join(output_dir, "fta_data.json")
        self.links_file = os.path.join(output_dir, "fta_links.json")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
    def run(self):
        """Main execution function"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                print(f"[{datetime.now()}] Checking US-Chile FTA for updates...")
                
                # Navigate to the US FTA page
                print(f"Navigating to {US_FTA_URL}")
                page.goto(US_FTA_URL, wait_until="networkidle")
                
                # Extract and store all links from the page
                links = self._extract_fta_links(page)
                self._save_links(links)
                
                # Check for changes in the FTA documents
                changes = self._check_for_changes(links)
                
                if changes:
                    print(f"[{datetime.now()}] Changes detected in the following documents:")
                    for doc, details in changes.items():
                        print(f"- {doc}: {details}")
                else:
                    print(f"[{datetime.now()}] No changes detected.")
                
            except Exception as e:
                print(f"Error during scraping: {e}")
            finally:
                browser.close()
    
    def _extract_fta_links(self, page):
        """Extract all relevant links from the FTA page"""
        links = {}
        
        # Get all links that might be related to FTA documents
        for path in PATHS_TO_MONITOR:
            try:
                # Try to find links by text (might need adjustment based on actual page structure)
                link_element = page.get_by_text(path, exact=True).first
                if link_element:
                    href = link_element.get_attribute("href")
                    if href:
                        full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
                        links[path] = {
                            "url": full_url,
                            "last_modified": None,
                            "hash": None
                        }
            except Exception as e:
                print(f"Could not find link for {path}: {e}")
        
        # If no links were found with the exact match approach, try a more general one
        if not links:
            all_links = page.evaluate("""() => {
                const allLinks = Array.from(document.querySelectorAll('a'));
                return allLinks.map(link => ({
                    text: link.innerText.trim(),
                    href: link.href
                }));
            }""")
            
            for link in all_links:
                for path in PATHS_TO_MONITOR:
                    if path.lower() in link["text"].lower():
                        links[path] = {
                            "url": link["href"],
                            "last_modified": None,
                            "hash": None
                        }
        
        print(f"Found {len(links)} relevant FTA document links")
        return links
    
    def _save_links(self, links):
        """Save extracted links to a JSON file"""
        with open(self.links_file, 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=2)
        print(f"Links saved to {self.links_file}")
    
    def _load_previous_data(self):
        """Load previously saved data for comparison"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_current_data(self, data):
        """Save current data for future comparisons"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _check_for_changes(self, links):
        """Check if any FTA documents have changed"""
        previous_data = self._load_previous_data()
        current_data = {}
        changes = {}
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            
            for doc_name, link_info in links.items():
                url = link_info["url"]
                try:
                    print(f"Checking document: {doc_name} at {url}")
                    
                    # Navigate to the document URL
                    page.goto(url, wait_until="networkidle")
                    
                    # Get the page content
                    content = page.content()
                    
                    # Calculate hash of the content
                    content_hash = hashlib.md5(content.encode()).hexdigest()
                    
                    # Get last modified info if available
                    last_modified = datetime.now().isoformat()
                    
                    # Store current data
                    current_data[doc_name] = {
                        "url": url,
                        "last_checked": datetime.now().isoformat(),
                        "last_modified": last_modified,
                        "hash": content_hash
                    }
                    
                    # Check if this document was in previous data
                    if doc_name in previous_data:
                        old_hash = previous_data[doc_name]["hash"]
                        if old_hash != content_hash:
                            changes[doc_name] = {
                                "status": "changed",
                                "previous_check": previous_data[doc_name]["last_checked"],
                                "current_check": current_data[doc_name]["last_checked"]
                            }
                    else:
                        changes[doc_name] = {
                            "status": "new",
                            "current_check": current_data[doc_name]["last_checked"]
                        }
                    
                    # Sleep briefly to avoid overloading the server
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error checking {doc_name}: {e}")
            
            browser.close()
        
        # Save current data for future comparisons
        self._save_current_data(current_data)
        
        return changes

def main():
    parser = argparse.ArgumentParser(description="FTA Scraper for Chile-US FTA")
    parser.add_argument("--output", default="./data", help="Directory to store output data")
    parser.add_argument("--no-headless", action="store_true", help="Run browser in visible mode")
    args = parser.parse_args()
    
    scraper = FTAScraper(
        output_dir=args.output,
        headless=not args.no_headless
    )
    
    scraper.run()

if __name__ == "__main__":
    main()