# Week 1: Agribusiness Data Analysis Planning

**Project**: Agribusiness Market Analytics & Forecasting Framework  
**Internship Role**: Data Scientist Intern  
**Repository**: `agribusiness-data-analysis`  
**Current Phase**: Week 1 – Research, Data Sourcing, and Analytical Planning  
**Date**: November 2026  
**Status**: Completed (Planning Phase Milestone)

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Project Objective](#2-project-objective)
3. [Business Context](#3-business-context)
4. [Research Questions](#4-research-questions)
5. [Proposed Data Sources](#5-proposed-data-sources)
6. [Data Source Comparison](#6-data-source-comparison)
7. [Key Metrics and KPIs](#7-key-metrics-and-kpis)
8. [Data Collection Strategy](#8-data-collection-strategy)
9. [Data Cleaning and Preprocessing Strategy](#9-data-cleaning-and-preprocessing-strategy)
10. [Exploratory Data Analysis Plan](#10-exploratory-data-analysis-plan)
11. [Statistical Analysis Plan](#11-statistical-analysis-plan)
12. [Forecasting Strategy](#12-forecasting-strategy)
13. [Expected Insights](#13-expected-insights)
14. [Risks and Limitations](#14-risks-and-limitations)
15. [Ethical and Data Quality Considerations](#15-ethical-and-data-quality-considerations)
16. [Project Timeline](#16-project-timeline)
17. [Technology Stack](#17-technology-stack)
18. [Reproducibility Plan](#18-reproducibility-plan)
19. [Conclusion](#19-conclusion)
20. [References](#20-references)

---

## 1. Executive Summary

Agriculture forms the backbone of food security, rural livelihoods, and industrial supply chains worldwide. In emerging economies like India, where agriculture engages over 45% of the national workforce and contributes approximately 16–18% to Gross Value Added (GVA), agricultural markets are exposed to intense price volatility, climate variability, and fragmented market linkages. Despite substantial advances in public data transparency, agricultural stakeholders—ranging from smallholder farmers and farmer producer organizations (FPOs) to agribusiness enterprises and food processors—frequently lack unified, data-driven frameworks to anticipate yield shifts, market arrival surges, and price fluctuations.

This report establishes the complete analytical architecture for a **six-week Agribusiness Data Science internship project**. The primary objective is to build an end-to-end data acquisition, cleaning, econometric evaluation, and predictive forecasting framework leveraging vetted, publicly available agricultural data sources (notably **data.gov.in**, the **Directorate of Economics and Statistics (DES)**, **Agmarknet**, **FAOSTAT**, and the **World Bank Open Data** portal). 

As a **Week 1 Planning Deliverable**, this document defines:
- A rigorous evaluation of 6 institutional agricultural data sources.
- 8 core business and research questions guiding agricultural supply-demand intelligence.
- 12 key performance indicators (KPIs) with exact mathematical formulations and business context.
- Modular Python pipelines for ingestion, defensive schema validation, cryptographic auditing, and data standardization.
- A future forecasting and evaluation protocol incorporating classical time-series (ARIMA/SARIMA), econometric decomposition, and feature-engineered machine learning models.

> **Methodological Note**: In accordance with rigorous scientific and ethical standards, this Week 1 report strictly differentiates between *existing public data systems*, *proposed analytical workflows*, *hypothesized/expected insights*, and *actual empirical findings*. No synthetic data has been fabricated, and no empirical conclusions are asserted prior to execution on validated raw records in subsequent project weeks.

---

## 2. Project Objective

The central objective is to design, implement, and validate an automated, modular Data Science platform for **agricultural commodity market analytics, spatial productivity mapping, and price forecasting**.

Specific tactical goals include:
1. **Harmonized Data Ingestion**: Establish robust, automated ingestion scripts capable of querying official open-data APIs and parsing multi-decadal government agricultural publications.
2. **Standardization & Preprocessing**: Engineer a fault-tolerant cleaning pipeline that reconciles disparate administrative units, historical district boundary shifts, divergent reporting units (quintals, tonnes, hectares, acres), and missing/anomalous observations.
3. **Spatial and Econometric Profiling**: Formulate comparative yield indices, cropping intensity metrics, and growth trajectories (CAGR/YoY) across major agro-climatic zones and commodity groups.
4. **Market Dynamics & Volatility Analysis**: Quantify the temporal dynamics of agricultural mandi arrivals, wholesale price spreads (Min-Max-Modal), and price volatility.
5. **Predictive Modeling Framework**: Formulate and benchmark baseline, statistical, and supervised machine learning time-series forecasting models to project monthly wholesale prices and annual crop production volumes.

---

## 3. Business Context

Agribusiness supply chains operate under high structural uncertainty. Unlike industrial manufacturing, agricultural production is characterized by biological gestation lags, inelastic short-run demand, seasonal harvesting cycles, and direct vulnerability to meteorological anomalies (monsoon rainfall, heat waves, unseasonal precipitation).

The business implications span multiple industry participants:

```
+---------------------------------------------------------------------------------------+
|                              Agribusiness Stakeholders                                |
+---------------------------+---------------------------+-------------------------------+
|    Producers & FPOs       |   Agribusiness & FMCG     |   Financial & Policy Bodies   |
| - Planting decisions      | - Procurement planning    | - Minimum Support Price (MSP) |
| - Optimal harvest timing  | - Inventory hedging       | - Warehousing & storage credit|
| - Mandi choice for sales  | - Supply chain continuity | - Inflation management        |
+---------------------------+---------------------------+-------------------------------+
```

1. **Agricultural Producers and FPOs**: Suffer from the "cobweb phenomenon" (hog cycle), where high prices in season $t$ trigger overplanting and gluts in season $t+1$, resulting in price collapses. Accurate seasonal arrival and price forecasting empowers farmers to make informed crop selection and storage decisions.
2. **Procurement Managers & Agribusiness Processors**: Large consumer goods and food processing corporations (milling, dairy, edible oils, starch) require accurate forward price visibility to optimize purchase orders, manage physical inventory, and hedge commodity contracts.
3. **Logistics & Warehousing Providers**: Warehousing corporations and cold chain operators require accurate projections of harvest volumes to position transport capacity and avoid post-harvest spillage.
4. **Policymakers and Credit Institutions**: Government agencies and agricultural rural banks require objective productivity benchmarks to target input subsidies, evaluate crop insurance claims (PMFBY), and formulate price stabilization interventions.

---

## 4. Research Questions

To deliver high-impact insights, the analytical framework addresses eight targeted research questions:

1. **Crop Yield Dynamics**: How have crop yields (kg/ha) for staple cereals, pulses, and oilseeds evolved across primary agricultural states over the past two decades, and which crops demonstrate sustained yield gains versus yield stagnation?
2. **Crop Portfolio & Volume Concentration**: Which crops account for the highest share of cultivated area and total production volume nationally and state-wise? What does this imply for crop diversification and regional specialization?
3. **Wholesale Commodity Price Fluctuations**: To what extent do wholesale market prices in APMC mandis fluctuate within and across marketing seasons, and how severe is price dispersion between minimum, maximum, and modal prices?
4. **Drivers of Production Variability**: How strongly are historical variations in crop output correlated with cultivated area expansion versus yield improvement (extensive vs. intensive margin of agricultural growth)?
5. **Regional Productivity Differentials**: Which agro-climatic regions and states consistently outperform national yield benchmarks, and which exhibit severe productivity deficits despite significant land allocation?
6. **Land Allocation vs. Production Efficiency**: How do land allocation patterns (Gross Cropped Area vs. Net Sown Area) correlate with regional agricultural output, and where does cropping intensity offer the greatest headroom for expansion?
7. **Seasonality and Arrival Elasticity**: What predictable seasonal cycles exist between post-harvest physical market arrivals and modal market prices? Does peak arrival correspond to an immediate price depression?
8. **Forecasting Feasibility**: Can historical price time series, seasonal lags, and arrival volumes be effectively modeled using classical econometrics (ARIMA/SARIMAX) or machine learning regressors to forecast future modal prices with acceptable error margins ($MAPE < 15\%$)?

---

## 5. Proposed Data Sources

To ensure scientific rigor and policy relevance, the project relies exclusively on authoritative, publicly accessible government and international institutional data repositories.

### Source 1: District-wise Crop Production Statistics (APY)
- **Organization**: Directorate of Economics & Statistics (DES), Department of Agriculture & Farmers Welfare, Ministry of Agriculture & Farmers Welfare, Government of India.
- **Access Portal**: Open Government Data (OGD) Platform India (`https://data.gov.in/resource/crop-production-statistics`) & DES Portal (`https://desagri.gov.in/`).
- **Geographic Coverage**: India (36 States & Union Territories, spanning over 700 administrative districts).
- **Temporal Coverage**: 1997–1998 to 2021–2022+ (Annual and Seasonal reporting).
- **Core Variables**: `State_Name`, `District_Name`, `Crop_Year`, `Season` (Kharif, Rabi, Summer, Autumn, Winter, Whole Year), `Crop`, `Area` (Hectares), `Production` (Metric Tonnes).
- **Format / API**: REST API via OGD India API Gateway; bulk CSV downloads.
- **Analytical Utility**: Foundational dataset for analyzing long-term spatial productivity, crop yield growth trends, land allocation shifts, and district-level performance indices.
- **Limitations**: District boundary splits over time (creation of new districts) introduce panel imbalances; occasional missing production records for minor crops.

### Source 2: Agmarknet Daily Wholesale Prices & Market Arrivals
- **Organization**: Directorate of Marketing & Inspection (DMI), Ministry of Agriculture & Farmers Welfare, Government of India.
- **Access Portal**: Agricultural Marketing Information Network (`https://agmarknet.gov.in/`).
- **Geographic Coverage**: National (Over 3,200 regulated wholesale agricultural markets / APMC mandis across India).
- **Temporal Coverage**: 2001 to Present (Daily transaction frequency).
- **Core Variables**: `State`, `District`, `Market` (Mandi name), `Commodity`, `Variety`, `Arrival_Date`, `Arrivals` (Tonnes), `Min_Price` (INR/Quintal), `Max_Price` (INR/Quintal), `Modal_Price` (INR/Quintal).
- **Format / API**: OGD India API endpoint (`https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070`), Web portal CSV/Excel exports.
- **Analytical Utility**: Essential for high-frequency price volatility modeling, arrival-price elasticity, seasonal price indices, and time-series forecasting.
- **Limitations**: Incomplete reporting by smaller or remote mandis on public holidays; non-trading days introduce intermittent temporal gaps.

### Source 3: Agricultural Statistics at a Glance
- **Organization**: Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers Welfare, Government of India.
- **Access Portal**: `https://desagri.gov.in/publication-category/agricultural-statistics-at-a-glance/`.
- **Geographic Coverage**: India (National and State aggregated levels).
- **Temporal Coverage**: 1950–1951 to Present (Annual compendiums).
- **Core Variables**: Long-term Area-Production-Yield of foodgrains and commercial crops, Minimum Support Prices (MSP) by crop year, Cost of Cultivation (A2, A2+FL, C2), Land Use Statistics (Net Sown Area, Gross Cropped Area).
- **Format / API**: PDF publication compendiums, accompanying downloadable Excel/CSV data tables.
- **Analytical Utility**: Establishing historical macroeconomic baselines, analyzing cropping intensity trends, comparing market prices against policy-mandated MSP benchmarks.
- **Limitations**: Published on an annual lag; predominantly available as aggregated tables requiring tabular parsing.

### Source 4: FAOSTAT – Crops and Livestock Products (QCL)
- **Organization**: Food and Agriculture Organization (FAO) of the United Nations.
- **Access Portal**: `https://www.fao.org/faostat/en/#data/QCL`.
- **Geographic Coverage**: Global (Over 245 countries and autonomous territories).
- **Temporal Coverage**: 1961 to 2022+ (Annual).
- **Core Variables**: `Country`, `Item` (Commodity), `Element` (Area harvested, Production, Yield), `Year`, `Unit` (ha, tonnes, kg/ha), `Value`, `Flag`.
- **Format / API**: FAOSTAT REST API (`https://fenixservices.fao.org/faostat/api/v1/`), Bulk CSV/ZIP download.
- **Analytical Utility**: Enables international benchmarking of domestic crop productivity against global averages and peer agrarian economies (e.g., China, Brazil, USA).
- **Limitations**: Aggregated at national level (no sub-national/state resolution); typically operates on an 18- to 24-month reporting lag.

### Source 5: World Bank Open Data – World Development Indicators (WDI)
- **Organization**: The World Bank Group.
- **Access Portal**: `https://data.worldbank.org/indicator`.
- **Geographic Coverage**: Global (217 economies and regional country groupings).
- **Temporal Coverage**: 1960 to Present (Annual).
- **Core Variables**: `AG.YLD.CREL.KG` (Cereal yield, kg/ha), `AG.LND.AGRI.ZS` (Agricultural land % of total land area), `NV.AGR.TOTL.ZS` (Agriculture, forestry, and fishing % of GDP), `AG.CON.FERT.ZS` (Fertilizer consumption per hectare of arable land).
- **Format / API**: World Bank Indicators REST API v2 (`https://api.worldbank.org/v2/country/...`), JSON, CSV.
- **Analytical Utility**: Contextualizing macroeconomic agricultural structural transformation, agricultural input intensity, and rural economic contributions.
- **Limitations**: Macro-level indicators only; lacks commodity-specific wholesale pricing.

### Source 6: USDA Foreign Agricultural Service (FAS) – PSD Database
- **Organization**: United States Department of Agriculture (USDA).
- **Access Portal**: `https://apps.fas.usda.gov/psdonline/app/index.html`.
- **Geographic Coverage**: Global commodity coverage for over 100 agricultural trading countries.
- **Temporal Coverage**: 1960 to Present (Annual marketing year series, updated monthly).
- **Core Variables**: `Commodity`, `Country`, `Market_Year`, `Beginning_Stocks`, `Production`, `Imports`, `Domestic_Consumption`, `Exports`, `Ending_Stocks`.
- **Format / API**: Custom CSV bulk downloads and FAS PSD API.
- **Analytical Utility**: Crucial for tracking global stock-to-use ratios, international supply balances, and import-export demand pressures on domestic commodity pricing.
- **Limitations**: Covers major commercial commodities (wheat, rice, corn, soybean, cotton); lacks minor regional pulses and perishables.

---

## 6. Data Source Comparison

The table below contrasts the technical characteristics of the candidate repositories:

| Dimension | DES / data.gov.in (APY) | Agmarknet (DMI) | DES Statistics at a Glance | FAOSTAT (QCL) | World Bank (WDI) | USDA FAS (PSD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Crop Output & Area | Wholesale Prices & Arrivals | Policy, MSP, Land Use | Global Production & Yield | Macroeconomic Agri Indicators | Global Supply & Balance Sheet |
| **Spatial Granularity** | District / State | Market (APMC Mandi) / District | National / State | National (Country) | National (Country) | National (Country) |
| **Temporal Frequency** | Seasonal / Annual | Daily | Annual | Annual | Annual | Annual / Monthly Updates |
| **Temporal Horizon** | 1997–2022+ (25+ yrs) | 2001–Present (20+ yrs) | 1950–Present (70+ yrs) | 1961–Present (60+ yrs) | 1960–Present (60+ yrs) | 1960–Present (60+ yrs) |
| **API Availability** | Yes (OGD API) | Yes (data.gov.in API) | No (Manual/Bulk) | Yes (REST API) | Yes (REST API v2) | Yes (FAS API) |
| **Primary File Format** | CSV, JSON | JSON, XML, CSV | XLSX, PDF, CSV | CSV, JSON | JSON, CSV, XML | CSV |
| **Access Restriction** | Public / Open Data | Public / Open Data | Public / Free Access | Public / CC BY-IGO 3.0 | Public / CC BY 4.0 | Public / US Gov Public Domain |
| **Core Role in Project** | **Core Panel 1 (Productivity)** | **Core Panel 2 (Pricing)** | **Benchmark & Policy Panel** | **Cross-Country Benchmark**| **Macro Context** | **Supply-Demand Balance** |

---

## 7. Key Metrics and KPIs

To translate raw datasets into actionable agribusiness intelligence, twelve primary metrics are mathematically formulated:

### 1. Crop Production ($P_{c,r,t}$)
- **Definition**: The total aggregate physical volume of a specific crop harvested within a designated geographic region and time period.
- **Formula**:
  $$\text{Production} = \sum_{i} \text{Output}_i \quad [\text{Expressed in Metric Tonnes (t)}]$$
- **Business Significance**: Fundamental measure of aggregate agricultural supply; determines raw material availability for food processing, export potential, and national buffer stocking.
- **Required Data**: Field harvest records, official production estimates from DES/data.gov.in.

### 2. Crop Yield ($Y_{c,r,t}$)
- **Definition**: The efficiency of agricultural production per unit of harvested land.
- **Formula**:
  $$Y_{c,r,t} = \frac{P_{c,r,t} \times 1000}{A_{c,r,t}} \quad [\text{Expressed in kg/hectare}]$$
  *(where $P$ is production in metric tonnes and $A$ is area in hectares)*
- **Business Significance**: Key indicator of land productivity and technological adoption (irrigation, high-yielding variety seeds, fertilization).
- **Required Data**: `Area` (ha) and `Production` (tonnes).

### 3. Cultivated Area ($A_{c,r,t}$)
- **Definition**: The total geographical land surface allocated to the cultivation of a specific crop within a season.
- **Formula**:
  $$A_{c,r,t} = \sum \text{Parcel Area} \quad [\text{Expressed in Hectares (ha)}]$$
- **Business Significance**: Reflects farmer planting intentions, acreage response to expected price signals, and land allocation changes.
- **Required Data**: `Area` (ha) reported by State Departments of Agriculture.

### 4. Production Growth Rate (YoY & CAGR)
- **Definition**: The annualized rate of change in crop production volume over single-year (YoY) and multi-year (CAGR) periods.
- **Formulas**:
  $$\text{YoY Growth } (\%) = \left( \frac{P_{c,r,t} - P_{c,r,t-1}}{P_{c,r,t-1}} \right) \times 100$$
  $$\text{CAGR } (t_0, t_n) = \left[ \left( \frac{P_{t_n}}{P_{t_0}} \right)^{\frac{1}{n}} - 1 \right] \times 100$$
- **Business Significance**: Evaluates long-term capacity expansion versus short-term output shocks (e.g., drought years).
- **Required Data**: Multi-year production time series.

### 5. Yield Growth Rate
- **Definition**: The rate of productivity improvement per unit area over time.
- **Formula**:
  $$\text{Yield YoY } (\%) = \left( \frac{Y_{c,r,t} - Y_{c,r,t-1}}{Y_{c,r,t-1}} \right) \times 100$$
- **Business Significance**: Differentiates between extensive production growth (clearing/allocating more land) and intensive growth (technological and agronomic efficiency).
- **Required Data**: Longitudinal yield series.

### 6. Commodity Modal Price ($Price_{\text{modal}}$)
- **Definition**: The wholesale price at which the highest transaction volume of a commodity traded in a designated APMC mandi on a given trading day.
- **Formula**:
  $$Price_{\text{modal}} = \text{mode}(Price_i) \quad [\text{Expressed in INR / Quintal (100 kg)}]$$
- **Business Significance**: Most representative price benchmark reflecting actual market clearing conditions, preferred over arithmetic mean which is distorted by extreme bids.
- **Required Data**: Daily APMC mandi transaction records from Agmarknet.

### 7. Price Volatility ($\sigma_{\text{returns}}$)
- **Definition**: The degree of dispersion and variation in commodity prices over a defined rolling window.
- **Formula**:
  $$r_t = \ln\left(\frac{Price_t}{Price_{t-1}}\right), \quad \sigma = \sqrt{\frac{1}{N-1} \sum_{t=1}^{N} (r_t - \bar{r})^2} \times \sqrt{k}$$
  *(where $k$ is the annualization factor, e.g., 252 for daily or 12 for monthly data)*
- **Business Significance**: Measures procurement price risk; informs financial hedging strategies, inventory buffer sizing, and working capital requirements.
- **Required Data**: Continuous daily or weekly price time series.

### 8. Year-over-Year (YoY) Price Change
- **Definition**: The percentage change in wholesale commodity price relative to the identical calendar month or week in the prior year.
- **Formula**:
  $$\Delta Price_{\text{YoY}} = \left( \frac{Price_{m, y} - Price_{m, y-1}}{Price_{m, y-1}} \right) \times 100$$
- **Business Significance**: Isolates structural inflation and market imbalances by controlling for regular within-year seasonal cycles.
- **Required Data**: Monthly aggregated modal price series.

### 9. Spatial Yield Index / Regional Productivity Index ($SYI$)
- **Definition**: The relative yield productivity of a specific district or state compared against the national or agro-climatic baseline for that crop.
- **Formula**:
  $$SYI_{d, c} = \left( \frac{Y_{d, c}}{\bar{Y}_{\text{national}, c}} \right) \times 100$$
- **Business Significance**: Identifies high-efficiency sourcing clusters and guides regional procurement prioritization for agribusinesses.
- **Required Data**: District-level and national-level crop yields.

### 10. Cropping Intensity Index ($CII$)
- **Definition**: The degree to which agricultural land is cropped multiple times within a single agricultural year.
- **Formula**:
  $$CII = \left( \frac{\text{Gross Cropped Area (GCA)}}{\text{Net Sown Area (NSA)}} \right) \times 100 \quad [\%]$$
- **Business Significance**: Reflects irrigation infrastructure coverage, double-cropping feasibility, and land-use efficiency.
- **Required Data**: Gross Cropped Area and Net Sown Area from Land Use Statistics (DES).

### 11. Seasonal Price Index ($SPI$)
- **Definition**: A standardized ratio reflecting the typical deviation of monthly prices from the centered annual trend.
- **Formula**:
  $$SPI_m = \left( \frac{\bar{Price}_m}{\bar{Price}_{\text{annual}}} \right) \times 100$$
- **Business Significance**: Guides seasonal timing of procurement contracts (e.g., purchasing during harvest trough vs. avoiding off-season peaks).
- **Required Data**: Multi-year monthly price series.

### 12. Market Arrival Elasticity of Price ($\varepsilon_{a}$)
- **Definition**: The sensitivity of wholesale modal price to changes in physical mandi arrival volume.
- **Formula**:
  $$\varepsilon_{a} = \frac{\% \Delta Price_{\text{modal}}}{\% \Delta Arrival_{\text{volume}}} = \frac{\partial \ln(Price)}{\partial \ln(Arrival)}$$
- **Business Significance**: Quantifies post-harvest price depression; indicates whether local mandis have adequate storage or experience distress-selling glut.
- **Required Data**: Concurrent daily arrival volume (tonnes) and modal price (INR/q).

---

## 8. Data Collection Plan

The data acquisition architecture is structured around four principles: **automation**, **validation**, **immutability**, and **provenance tracking**.

```
+---------------------------------------------------------------------------------------+
|                               Data Acquisition Pipeline                               |
+-------------------+   +--------------------+   +-------------------+   +--------------+
| 1. Discovery &    |-->| 2. Programmatic    |-->| 3. Ingestion &    |-->| 4. Provenance|
| Endpoint Registry |   | Querying / Extract |   | Schema Validation |   | Manifest Log |
+-------------------+   +--------------------+   +-------------------+   +--------------+
```

### Step-by-Step Acquisition Process

1. **Dataset Discovery & Cataloging**:
   - Register official endpoints, query parameters, rate limits, and authentication keys in a centralized configuration dictionary.
   - Maintain source provenance metadata in `data/README.md`.

2. **Programmatic Data Download**:
   - Implement dedicated client classes in `src/data_collection.py` (`WorldBankAgriCollector`, `LocalDatasetIngestor`).
   - Use `requests` sessions configured with retry logic, exponential backoff, and strict timeout parameters (30 seconds) to ensure reliable acquisition over unstable connections.

3. **Multi-Format Ingestion**:
   - Ingest tabular CSV/Excel files using `pandas.read_csv` and `openpyxl` with explicit encoding specifications (`utf-8` or `latin1`).
   - Parse nested JSON payloads from REST APIs (World Bank, data.gov.in) into standardized tabular formats.

4. **Source Validation & Schema Enforcement**:
   - Inspect column contracts immediately upon download. Verify mandatory columns (e.g., `State_Name`, `Crop_Year`, `Production`).
   - Compute diagnostic profiles (`total_records`, `missing_cells`, `duplicate_rows`) via `inspect_raw_dataset()`.

5. **Data Storage & Immutability**:
   - Store all unaltered source files in `data/raw/`. 
   - Strict policy: Files in `data/raw/` are treated as read-only snapshots and never modified in place.

6. **Data Versioning & Cryptographic Audit**:
   - Automatically compute SHA-256 cryptographic hashes for every ingested raw file using `src.utils.calculate_sha256()`.
   - Update `data/raw/manifests/audit_log.json` with file size, row counts, acquisition timestamp, source URL, and SHA-256 digest to establish an unbroken audit trail.

---

## 9. Data Cleaning and Preprocessing Strategy

Raw agricultural administrative datasets frequently contain naming inconsistencies, spatial boundary changes, and reporting artifacts. The cleaning strategy executes in `src/data_cleaning.py`:

```
+---------------------------------------------------------------------------------------+
|                             Data Cleaning & Harmonization                             |
+-------------------+   +--------------------+   +-------------------+   +--------------+
| 1. Structural &   |-->| 2. Taxonomic &     |-->| 3. Outlier        |-->| 4. Feature   |
| Deduplication     |   | Entity Mapping     |   | Detection & Bounds|   | Engineering  |
+-------------------+   +--------------------+   +-------------------+   +--------------+
```

### Preprocessing Protocol & Justification

1. **Handling Missing Values**:
   - *Area & Production Nulls*: If both `Area` and `Production` are missing or zero, the record is uninformative and dropped. If `Area > 0` but `Production` is null, record is segregated; for longitudinal district series, missing production is imputed using median yield of the same district-crop-season within a 3-year rolling window.
   - *Mandi Price Gaps*: Non-trading days (weekends, holidays) are maintained as explicit date indices and forward-filled (up to a 3-day maximum) to preserve continuity for time-series models.

2. **Deduplication on Composite Keys**:
   - Administrative reporting occasionally results in duplicate rows. Records are deduplicated against composite primary keys: `['state_name', 'district_name', 'crop_year', 'season', 'crop']` for APY data, and `['state', 'district', 'market', 'commodity', 'variety', 'arrival_date']` for Agmarknet data.

3. **Data Type Coercion & Whitespace Normalization**:
   - Clean column headers to lowercase `snake_case`. Strip leading/trailing whitespaces.
   - Remove comma separators from formatted numeric strings (e.g., `"1,250.50"` $\rightarrow$ `1250.50`). Convert date strings to ISO 8601 `datetime64[ns]`.

4. **Taxonomic & Crop Name Standardization**:
   - Resolve semantic fragmentation where identical crops are entered under dialectal or trade names.
   - Map aliases using a canonical dictionary: `"Paddy"` $\rightarrow$ `"Rice"`, `"Gram"` $\rightarrow$ `"Chickpea"`, `"Arhar/Tur"` $\rightarrow$ `"Pigeonpea"`, `"Groundnut"` $\rightarrow$ `"Peanut"`.
   - Assign standardized category hierarchies: `Cereals`, `Pulses`, `Oilseeds`, `Commercial`, `Horticulture`.

5. **Geographic Name Harmonization**:
   - Normalize historical state nomenclature (e.g., `"Orissa"` $\rightarrow$ `"Odisha"`, `"Uttaranchal"` $\rightarrow$ `"Uttarakhand"`, `"Pondicherry"` $\rightarrow$ `"Puducherry"`).
   - Flag district reorganizations to maintain panel integrity across decadal comparisons.

6. **Unit Standardization**:
   - Enforce uniform metric units across all tables: Area in **Hectares (ha)**, Production in **Metric Tonnes (t)**, Yield in **kg/ha**, and Commodity Prices in **INR / Quintal (100 kg)**.
   - Apply explicit conversion factors where raw tables report in acres, bushels, or quintals.

7. **Outlier Detection & Biological Bounds**:
   - Implement a dual-layer anomaly filter:
     - *Layer 1 (Biological Feasibility)*: Flag records that violate physical agronomic yield ceilings (e.g., cereal yield $< 100\text{ kg/ha}$ or $> 15,000\text{ kg/ha}$; pulse yield $> 4,500\text{ kg/ha}$).
     - *Layer 2 (Statistical Dispersion)*: Flag observations exceeding $Q_{75} + 3.0 \times IQR$ within specific crop distributions.
   - Anomalies are retained with an explicit boolean flag (`is_outlier = True`) and reason logged, rather than silently erased.

8. **Feature Engineering**:
   - Construct analytical features: lag variables ($t-1, t-3, t-12\text{ months}$), rolling moving averages ($MA_{7}, MA_{30}, MA_{90}$), rolling price volatility, and calendar attributes (`month`, `quarter`, `harvest_season_flag`).

---

## 10. Exploratory Data Analysis Plan

The exploratory data analysis phase will examine distributional patterns, spatial clustering, and time dynamics:

### Planned Visualizations & Analyses

1. **Univariate Analysis**:
   - *Yield & Production Distributions*: Histograms with kernel density estimates (KDE) and box plots to assess skewness, kurtosis, and modal productivity across major crop classifications.
   - *Price Spread Distributions*: Box plots of minimum, maximum, and modal wholesale prices across major commodities.

2. **Bivariate Analysis**:
   - *Area vs. Production Elasticity*: Log-log scatter plots with OLS regression fits ($\ln(P) = \alpha + \beta \ln(A) + \varepsilon$) to evaluate returns to scale in acreage allocation.
   - *Arrival vs. Modal Price Elasticity*: Scatter plots of daily physical mandi arrivals against modal prices to observe supply curve clearing.

3. **Time-Series Trajectory Analysis**:
   - *Longitudinal Yield & Production Trends*: Multi-line charts tracking national and state-level production trajectories (1997–2022).
   - *Modal Price Trajectories*: Time-series plots overlaying daily/monthly wholesale prices with Minimum Support Price (MSP) benchmarks.

4. **Regional & Spatial Comparative Analysis**:
   - *Spatial Productivity Choropleths*: Geographic heatmaps mapping District Spatial Yield Indices ($SYI$) to visually identify agricultural high-productivity belts versus distress regions.
   - *State-level Crop Portfolio Breakdown*: Stacked horizontal bar charts comparing the top 10 producing states for major staple commodities.

5. **Seasonality and Cyclic Profiling**:
   - *Monthly Price Seasonality Index Plots*: Radar / polar charts and sub-annual monthly line graphs showing systematic harvest arrival dips and pre-harvest price surges.

6. **Correlation Analysis**:
   - *Multivariate Correlation Heatmaps*: Pearson and Spearman rank correlation matrices examining relationships between cultivated area, production, yield, price volatility, and macroeconomic indicators.

---

## 11. Statistical Analysis Plan

All empirical testing will be conducted using rigorous econometric and statistical techniques in `src/analysis.py`:

```
+---------------------------------------------------------------------------------------+
|                             Statistical Analysis Pipeline                             |
+-------------------+   +--------------------+   +-------------------+   +--------------+
| 1. Descriptive    |-->| 2. Hypothesis      |-->| 3. Stationarity   |-->| 4. Econometric|
| Parametric & Non-P|   | Testing (ANOVA, t) |   | Testing (ADF/KPSS)|   | Decomposition|
+-------------------+   +--------------------+   +-------------------+   +--------------+
```

1. **Descriptive Summary Profiling**:
   - Calculate parametric metrics (mean, standard deviation, variance) and non-parametric robust statistics (median, interquartile range, median absolute deviation) for every continuous variable.
   - Evaluate distribution symmetry via Fisher-Pearson skewness and kurtosis coefficients.

2. **Hypothesis Testing**:
   - *One-Way ANOVA / Kruskal-Wallis Test*: Test the null hypothesis ($H_0$) that mean crop yields are equal across agro-ecological zones versus the alternative ($H_1$) that significant spatial productivity differentials exist.
   - *Welch's Two-Sample t-test / Mann-Whitney U Test*: Evaluate whether irrigated vs. rainfed crop yields exhibit statistically significant differences under anomalous rainfall years.
   - *Significance Threshold*: Standard $\alpha = 0.05$ with Bonferroni correction for multi-hypothesis comparisons.

3. **Time-Series Stationarity Verification**:
   - Agricultural commodity prices and production series typically exhibit stochastic trends and non-stationarity.
   - Conduct **Augmented Dickey-Fuller (ADF)** tests:
     $$\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^{p} \delta_i \Delta y_{t-i} + \varepsilon_t$$
     where rejecting $H_0: \gamma = 0$ confirms stationarity.
   - Complement with the **KPSS (Kwiatkowski-Phillips-Schmidt-Shin)** test to differentiate between unit-root non-stationarity and trend-stationarity.
   - Apply first-differencing or seasonal differencing ($\Delta_{12}$) as dictated by test outcomes.

4. **Time-Series Decomposition**:
   - Decompose historical mandi prices into trend-cycle ($T_t$), seasonal ($S_t$), and irregular/residual components ($I_t$):
     $$\text{Additive Model}: Y_t = T_t + S_t + I_t$$
     $$\text{Multiplicative Model}: Y_t = T_t \times S_t \times I_t$$
   - Apply **Seasonal-Trend Decomposition using LOESS (STL)** to accommodate evolving seasonal patterns over decadal horizons.

5. **Panel Regression Analysis**:
   - Estimate pooled OLS and Fixed Effects panel models to evaluate yield determinants:
     $$Y_{i, t} = \beta_0 + \beta_1 \text{Area}_{i, t} + \beta_2 \text{Trend}_t + \mu_i + \varepsilon_{i, t}$$
     where $\mu_i$ controls for unobserved, time-invariant district-specific agro-climatic endowments.

---

## 12. Forecasting Strategy

The predictive forecasting phase (scheduled for Weeks 4 and 5) will model future wholesale commodity prices and regional production levels.

### Model Candidates & Selection Rationale

| Model Family | Technique | Applicable Target | Input Requirements | Primary Strengths | Inherent Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline Benchmarks** | Naïve / Seasonal Naïve / Moving Average | Monthly Prices / Annual Output | Target historical series only | Costless, transparent baseline; essential hurdle for complex models | Cannot capture structural inflection points or trends |
| **Classical Econometric** | **ARIMA / SARIMA** | Monthly Modal Price Series | Stationary, univariate price series | Rigorous statistical foundation; explicitly models autoregression and seasonality | Linear assumptions; sensitive to structural market regime shifts |
| **Dynamic Smoothing** | **Holt-Winters Exponential Smoothing** | Monthly Prices & Arrivals | Level, trend, and seasonal components | Computationally efficient; adapts weighting rapidly to recent shifts | Degrades rapidly over multi-step forward forecast horizons ($h > 6$) |
| **Supervised Machine Learning** | **Random Forest / XGBoost Regressor** | Commodity Price & Production | Tabular feature matrix (lags, rolling stats, rainfall anomalies) | Captures non-linear feature interactions; handles multi-variate exogenous drivers | Risk of overfitting on short agrarian series; requires strict temporal cross-validation |

### Evaluation Protocol & Metrics

To avoid look-ahead bias and data leakage, all model evaluation will use **Temporal Walk-Forward Cross-Validation** (Expanding Window Rolling Forecasts) rather than randomized k-fold splits.

```
Train: [2010 ------------ 2018] -> Validate: [2019]
Train: [2010 --------------------- 2019] -> Validate: [2020]
Train: [2010 -------------------------------- 2020] -> Validate: [2021]
```

Models will be assessed across four standardized error metrics:

1. **Mean Absolute Error (MAE)**:
   $$\text{MAE} = \frac{1}{n} \sum_{t=1}^{n} |y_t - \hat{y}_t| \quad [\text{In native units: INR/q or Tonnes}]$$
2. **Root Mean Squared Error (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{t=1}^{n} (y_t - \hat{y}_t)^2} \quad [\text{Penalizes large outlier forecast errors}]$$
3. **Mean Absolute Percentage Error (MAPE)**:
   $$\text{MAPE} = \left(\frac{1}{n} \sum_{t=1}^{n} \left|\frac{y_t - \hat{y}_t}{y_t}\right|\right) \times 100 \quad [\%]$$
4. **Symmetric Mean Absolute Percentage Error (sMAPE)**:
   $$\text{sMAPE} = \left(\frac{1}{n} \sum_{t=1}^{n} \frac{|\hat{y}_t - y_t|}{(|y_t| + |\hat{y}_t|) / 2}\right) \times 100 \quad [\% \text{ bounded between } 0 \text{ and } 200\%]$$

---

## 13. Expected Insights

Based on agribusiness economic theory and preliminary domain literature, the following structural patterns are hypothesized to emerge from empirical execution in Weeks 3–5:

1. **Spatial Yield Polarization**: Substantial productivity gaps are expected between well-irrigated northwestern agro-climatic zones (Punjab, Haryana) and rainfed central/eastern belts for staple cereals (wheat, rice), with irrigated zones showing higher mean yield but lower year-to-year coefficient of variation ($CV$).
2. **Crop Portfolio Specialization**: District-level land allocation is anticipated to demonstrate high concentration in staple cereal-cereal rotations (Rice-Wheat) in the Indo-Gangetic Plains, contrasted with volatile pulses and oilseeds acreage in central arid regions driven by rainfall timing.
3. **Pronounced Price Seasonality**: Perishable commodities (onion, potato, tomato) are expected to display extreme seasonal amplitude ($SPI$ fluctuating $\pm 40\%$ from annual mean), characterized by sharp harvest troughs followed by pre-monsoon price escalations.
4. **Arrival-Price Asymmetry**: Mandi modal prices are hypothesized to exhibit asymmetric price transmission, where surge arrivals depress wholesale prices rapidly, but arrival shortfalls take multiple periods to translate into retail price transmission.
5. **Acreage vs. Yield Contributions**: Over the 25-year panel, total production growth in cereals is anticipated to be predominantly yield-driven (intensive margin), while pulse production growth may reflect higher sensitivity to area allocation (extensive margin).

---

## 14. Risks and Limitations

| Risk Dimension | Description | Analytical Mitigation Strategy |
| :--- | :--- | :--- |
| **Administrative Boundary Changes** | Bifurcation of Indian districts (e.g., creation of new districts) creates artificial discontinuities in longitudinal panels. | Harmonize district boundaries back to Census 2001/2011 baseline polygons using spatial concordance crosswalks. |
| **Reporting Gaps in Mandi Data** | Smaller mandis experience missing daily price reporting during local holidays or infrastructure outages. | Aggregate daily transactions to weekly/monthly weighted modal benchmarks; enforce minimum transaction frequency thresholds. |
| **Measurement & Entry Errors** | Typographical data entry errors in manual mandi submissions (e.g., extra zero in price or yield). | Implement automated two-tier biological feasibility and $3 \times IQR$ anomaly flagging prior to analytical aggregation. |
| **Structural Market Breaks** | Exogenous shocks (export bans, demonetization, COVID-19 lockdown supply disruptions, import tariff revisions) disrupt time series. | Include intervention indicator dummy variables ($D_{\text{shock}}$) in econometric and forecasting models. |
| **Look-Ahead Bias in ML Models** | Inadvertent leakage of future data into lag features or imputation steps. | Strict temporal walk-forward split protocol; all feature scaling and imputation fit strictly on training slices. |

---

## 15. Ethical and Data Quality Considerations

1. **Attribution and Open-Data Licensing**:
   - All datasets utilized in this project are governed by official open-access licenses (e.g., *Government Open Data License - India (GODL)*, *Creative Commons Attribution 4.0 International* for World Bank, and *CC BY-IGO 3.0* for FAOSTAT).
   - Clear citations, source URLs, and original institutional attributions are preserved across all documentation and code manifests.

2. **Responsible Analytical Reporting**:
   - In agricultural economics, premature or fabricated price forecasts can induce speculative behavior or mislead farm planning. This project maintains complete transparency regarding model error bounds (MAE/MAPE) and refrains from presenting experimental forecasts as commercial recommendations.

3. **Data Integrity & Traceability**:
   - Cryptographic SHA-256 hashes generated at ingestion prevent undetected tampering or bit rot.
   - Raw records remain unaltered, ensuring third-party reviewers can audit intermediate transformations.

---

## 16. Project Timeline

The 6-week internship schedule is structured sequentially:

```
+---------------------------------------------------------------------------------------------------------+
|                                    6-Week Internship Project Roadmap                                    |
+---------+-------------------------------------------------------------+---------------------------------+
| Week    | Milestone & Deliverables                                    | Status                          |
+---------+-------------------------------------------------------------+---------------------------------+
| Week 1  | Research, Data-Source Identification & Analytical Planning  | COMPLETED (Current Deliverable) |
| Week 2  | Programmatic Ingestion, Profiling & Pipeline Cleaning       | UPCOMING (Ready for Execution)  |
| Week 3  | Exploratory Data Analysis & Statistical Hypothesis Testing  | Scheduled                       |
| Week 4  | Econometric Time-Series & Forecasting Model Development     | Scheduled                       |
| Week 5  | Model Validation, Residual Diagnostics & Visualization      | Scheduled                       |
| Week 6  | Final Synthesis Report, Interactive Dashboard & Presentation| Scheduled                       |
+---------+-------------------------------------------------------------+---------------------------------+
```

### Detailed Milestone Breakdown

- **Week 1: Research, Data-Source Identification & Analytical Planning** *(Completed)*
  - Survey and validate 6 institutional public data portals.
  - Define 8 core research questions and 12 agribusiness KPIs.
  - Establish GitHub repository architecture, `.gitignore`, and `requirements.txt`.
  - Author modular Python scaffolding for data acquisition, cleaning, and analysis.
  - Submit formal Week 1 Planning Report.

- **Week 2: Data Collection, Profiling, and Data Cleaning**
  - Execute API ingestion batches for World Bank and data.gov.in resources.
  - Ingest multi-decadal APY district-level dataset and APMC mandi price series.
  - Run `src.data_cleaning` pipeline to standardize crop names, resolve missing values, and flag anomalies.
  - Generate cleaned analysis-ready Parquet tables in `data/processed/`.

- **Week 3: Exploratory Data Analysis, Feature Engineering & Statistical Testing**
  - Execute comprehensive univariate, bivariate, and spatial EDA in Notebook `03_initial_eda.ipynb`.
  - Compute descriptive statistics, CAGR, and volatility metrics across major crops.
  - Conduct ANOVA tests across agro-climatic zones and Augmented Dickey-Fuller stationarity tests.
  - Generate correlation matrices and seasonal price decomposition plots.

- **Week 4: Econometric & Machine Learning Forecasting**
  - Implement baseline forecasting models (Naïve, Seasonal Naïve, Moving Average).
  - Train ARIMA and Seasonal ARIMA (SARIMAX) models on priority commodity prices.
  - Engineer lag features and rolling statistics for supervised ML models (Random Forest / XGBoost).
  - Execute temporal walk-forward validation splits.

- **Week 5: Model Evaluation, Interpretation & Sensitivity Diagnostics**
  - Compute comparative forecast evaluation metrics (MAE, RMSE, MAPE, sMAPE).
  - Plot actual vs. predicted price trajectories with confidence bands.
  - Perform residual diagnostics (Ljung-Box test for autocorrelation, Q-Q plots for normality).
  - Conduct scenario sensitivity analyses against simulated supply-side shocks.

- **Week 6: Final Synthesis, Dashboard & Documentation**
  - Compile the comprehensive End-of-Internship Technical Report.
  - Build an interactive visual dashboard (Streamlit / Matplotlib panel) for commodity price exploration.
  - Package all code, manifests, and documentation for public open-source release.
  - Present findings to the internship evaluation committee.

---

## 17. Technology Stack

The project relies on a focused Python data science stack:

```
+---------------------------------------------------------------------------------------+
|                                Technology Architecture                                |
+---------------------------------------------------------------------------------------+
|  Environment & Execution  | Python 3.10+, Jupyter Notebook, Git & GitHub              |
|  Ingestion & Transport    | Requests, Urllib3, OpenPyXL, PyArrow                      |
|  Data Processing & Wrangling| Pandas (v2.0+), NumPy (v1.24+)                          |
|  Statistical & Econometric| SciPy, Statsmodels (v0.14+), Scikit-Learn (v1.3+)         |
|  Visual Analytics         | Matplotlib (v3.7+), Seaborn (v0.12+)                      |
+---------------------------------------------------------------------------------------+
```

---

## 18. Reproducibility Plan

To ensure that every analytical output and figure can be independently replicated:

1. **Standardized Environment**: All dependencies are locked with version bounds in `requirements.txt`.
2. **Directory Conventions**: Hardcoded absolute paths are prohibited; all scripts dynamically resolve relative paths from the repository root via `pathlib.Path`.
3. **Data Provenance**: Ingested raw datasets are cataloged with SHA-256 cryptographic hashes in `data/raw/manifests/audit_log.json`.
4. **Deterministic Random Seeds**: All stochastic procedures (cross-validation, model initialization) will set an explicit global random seed (`random_state=42`).
5. **Execution Order**: Notebooks follow a numbered execution hierarchy (`01_...` $\rightarrow$ `02_...` $\rightarrow$ `03_...`).

---

## 19. Conclusion

This Week 1 Planning deliverable provides an empirically grounded blueprint for executing an agribusiness data science study. By anchoring the analytical design in official public data systems—specifically Indian district agricultural statistics, national APMC mandi price feeds, FAOSTAT, and World Bank indicators—the project establishes a sound foundation for addressing critical questions in crop productivity, price stability, and agricultural forecasting.

With the repository scaffolding, defensive ingestion clients, cleaning pipelines, and KPI functions built in `src/`, the project is positioned to execute Week 2 data collection and preprocessing without ambiguity.

---

## 20. References

1. **Directorate of Economics & Statistics (DES)** (2022). *Agricultural Statistics at a Glance 2021*. Department of Agriculture & Farmers Welfare, Ministry of Agriculture & Farmers Welfare, Government of India. New Delhi.
2. **Directorate of Marketing & Inspection (DMI)** (2026). *Agmarknet Portal: Wholesale Agricultural Commodity Prices & Arrivals*. Ministry of Agriculture & Farmers Welfare, Government of India. `https://agmarknet.gov.in/`
3. **Food and Agriculture Organization of the United Nations (FAO)** (2024). *FAOSTAT Statistical Database: Crops and Livestock Products (QCL)*. Rome: FAO. `https://www.fao.org/faostat/en/#data/QCL`
4. **Government of India** (2026). *Open Government Data (OGD) Platform India: Crop Production Statistics*. `https://data.gov.in/resource/crop-production-statistics`
5. **The World Bank** (2026). *World Development Indicators: Agriculture & Rural Development*. Washington, D.C.: World Bank Group. `https://data.worldbank.org/indicator`
6. **United States Department of Agriculture (USDA) Foreign Agricultural Service** (2026). *Production, Supply and Distribution (PSD) Online Database*. Washington, D.C.: USDA FAS. `https://apps.fas.usda.gov/psdonline/`
7. **Hyndman, R.J., & Athanasopoulos, G.** (2018). *Forecasting: Principles and Practice*, 2nd Edition. OTexts: Melbourne, Australia.
8. **Acharya, S.S., & Agarwal, N.L.** (2016). *Agricultural Marketing in India*, 6th Edition. Oxford & IBH Publishing Co. Pvt. Ltd., New Delhi.
