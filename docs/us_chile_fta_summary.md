# US-Chile Free Trade Agreement Analysis

## Step 1: Finding the Chile Customs Website
The official website for the Chilean National Customs Service (Servicio Nacional de Aduanas) is:
- URL: https://www.aduana.cl

## Step 2: Finding the Free Trade Agreements Page
The Free Trade Agreements page can be found through the "Acuerdos y Tratados" (Agreements and Treaties) section of the website:
- URL: https://www.aduana.cl/aduana/site/edic/base/port/acuerdos_y_tratados.html

## Step 3: Finding the US-Chile FTA Documents
The US-Chile Free Trade Agreement page is located at:
- URL: https://www.aduana.cl/tratado-de-libre-comercio-chile-estados-unidos/aduana/2007-02-28/165004.html

### Key Documents Found:
1. **Rules of Origin Chapter 4** - Main text defining origin criteria
   - URL: https://www.aduana.cl/aduana/site/docs/20070711/20070711153552/reglas_de_origen_capitulo_cuatro.pdf

2. **Specific Rules of Origin Original Text (Annex 4.1)** - Defines specific origin rules by tariff classification
   - URL: https://www.aduana.cl/aduana/site/docs/20070711/20070711153552/04_anexo_reglas_especificas_origen.pdf

3. **Amendments to Annex 4.1**:
   - Decree No. 28 of 2008 (D.O. 27.03.2008)
   - Decree No. 117 of 2011 (D.O. 23.12.2011)
   - Note S/N of 2011 (D.O. 30.12.2011)
   - Decree No. 130 of 2012 (D.O. 11.05.2013)
   - Decree No. 17 of 2020 (D.O. 21.07.2020)

4. **Common Guidelines** - Resolution No. 342 DNA from 2015
   - URL: https://www.aduana.cl/aduana/site/docs/20070711/20070711153552/res342_15___directrices_comunes.pdf

5. **Additional Circular Documents**:
   - Circular No. 225 (21.07.2020)
   - Circular No. 119 (10.04.2015)
   - Circular No. 033 (29.01.2015)
   - Circular No. 290 (06.10.2014)
   - Circular No. 139 (23.05.2013)
   - Circular No. 123 (27.04.2009)
   - Circular No. 53 (07.02.2005)
   - Circular No. 27 (27.01.2004) - About filling out the Certificate of Origin
   - Circular No. 333 (18.12.2003) - Norms for applying the Chile-US FTA

## Structure of Rules of Origin (Chapter 4)
The document is divided into two main sections:
- **Section A - Rules of Origin**: Articles 4.1 to 4.11, covering:
  - Definition of "originating goods"
  - Regional value content calculation methods
  - Treatment of materials, accessories, and fungible goods
  - Accumulation provisions
  - De minimis rule
  - Transit and transshipment rules

- **Section B - Origin Procedures**: Articles 4.12 onwards, covering:
  - Origin declaration procedures
  - Certificate of Origin requirements
  - Record keeping and verification

## HTS Codes Impact
The Annex 4.1 contains specific rules of origin organized by HS chapter (01-97). Each chapter has specific requirements that products must meet to qualify as originating. The rules typically involve:
1. Change in tariff classification requirements
2. Regional value content requirements
3. Specific production processes requirements

## Certificate of Origin Requirements
According to Article 4.13, a certificate of origin:
- Can be issued by the importer, exporter, or producer
- No required format, but must include specific information
- May be submitted electronically
- Can cover a single shipment or multiple shipments of identical goods

## Automation Strategy
An automation script was created to monitor the Chilean Customs website for any changes to the US-Chile FTA documents. The script:
1. Navigates to the US-Chile FTA page
2. Extracts links to all relevant documents
3. Downloads and hashes the content of each document
4. Compares with previous versions to detect changes
5. Logs and reports any detected modifications

This allows for continuous monitoring of amendments, updates to rules of origin, or any other changes to the agreement that might affect trade between the countries.