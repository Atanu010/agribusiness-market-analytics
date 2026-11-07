# Agribusiness Market Analytics & Forecasting Platform

[![Current Milestone: Week 1 – Planning Phase](https://img.shields.io/badge/Milestone-Week%201%20%7C%20Planning%20Phase-blue.svg)](file:///c:/Users/bhowm/OneDrive/Documents/GitHub/agribusiness-market-analytics/reports/week1_agribusiness_data_analysis_plan.md)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> **Project Phase**: **Week 1 – Planning Phase**  
> **Role**: Data Scientist Intern  
> **Repository**: `agribusiness-data-analysis`  
> **Primary Deliverable**: [Week 1 Agribusiness Data Analysis Planning Report](file:///c:/Users/bhowm/OneDrive/Documents/GitHub/agribusiness-market-analytics/reports/week1_agribusiness_data_analysis_plan.md)

---

## 1. Project Overview

Agriculture and agribusiness represent the cornerstone of food security and economic stability across emerging and developed economies alike. However, agricultural markets are routinely subjected to acute commodity price volatility, harvest seasonality, spatial productivity disparities, and climatic risks.

This repository hosts a multi-week Data Science internship project dedicated to designing and building a reproducible, research-backed analytics platform. The project systematically ingests, harmonizes, analyzes, and forecasts publicly available agricultural datasets from premier national and international statistical bodies.

```
+---------------------------------------------------------------------------------------------------------+
|                                    End-to-End Agribusiness Analytics                                   |
+-------------------+   +--------------------+   +-------------------+   +--------------------------------+
| Public Data Sourcing  |-->| Ingestion & Schema |-->| Econometric & EDA |-->| Time-Series Forecasting        |
| - DES / data.gov.in|   | - Validation rules |   | - Yield metrics   |   | - ARIMA / SARIMA               |
| - Agmarknet Prices |   | - Anomaly flagging |   | - Seasonality     |   | - ML Regressors (XGBoost/RF)   |
| - FAOSTAT & WorldBank | - SHA-256 manifests|   | - Volatility      |   | - Walk-Forward Evaluation      |
+-------------------+   +--------------------+   +-------------------+   +--------------------------------+
```

---

## 2. Project Objective

The primary objective is to develop a modular, end-to-end Python pipeline to:
1. **Harmonize Public Agricultural Data**: Bridge multi-decadal district crop production panels (APY) with daily wholesale mandi price series (Agmarknet) and macroeconomic benchmarks (FAOSTAT, World Bank).
2. **Quantify Agribusiness KPIs**: Calculate production growth, spatial yield indices, price volatility, and cropping intensity to understand long-term agricultural trends.
3. **Analyze Market Dynamics**: Uncover seasonal arrival patterns, spatial price transmission, and yield determinants across diverse agro-climatic zones.
4. **Develop Predictive Forecasts**: Formulate and validate econometric and machine learning forecasting models to project commodity prices and annual output with rigorous out-of-sample evaluation.

> **Integrity Notice**: In accordance with rigorous scientific standards, Week 1 focuses strictly on research, source cataloging, pipeline architecture, and methodology design. No synthetic datasets, fabricated results, or unsupported empirical claims are presented prior to live batch execution in subsequent weeks.

---

## 3. Core Research Questions

The project addresses eight targeted agribusiness and research questions:

1. **Crop Yield Trajectories**: How have crop yields (kg/ha) evolved over the last 25 years for staple foodgrains, pulses, and oilseeds across primary producing states?
2. **Production Concentration**: Which crops dominate national and state-level agricultural output, and how diverse is regional crop allocation?
3. **Price Dispersion & Volatility**: How severely do wholesale prices fluctuate across marketing seasons, and what characterizes the spread between minimum, maximum, and modal prices?
4. **Extensive vs. Intensive Growth**: Is production growth predominantly driven by cultivated acreage expansion or intensive technological yield improvement?
5. **Spatial Productivity Disparities**: Which agro-climatic regions consistently exceed national productivity benchmarks, and where do severe yield deficits persist?
6. **Land Allocation & Cropping Intensity**: How does cropping intensity (Gross Cropped Area / Net Sown Area) vary geographically, and where can double-cropping expand?
7. **Seasonality & Arrival Elasticities**: What empirical relationships exist between post-harvest physical market arrivals and modal price troughs?
8. **Forecasting Feasibility**: Can historical price time series and seasonal features reliably forecast wholesale prices using ARIMA/SARIMA and machine learning regressors within an acceptable error margin ($MAPE < 15\%$)?

---

## 4. Planned Data Sources

All datasets utilized in this project are acquired exclusively from official public government portals and multilateral organizations:

| Source Identifier | Organization | Coverage & Frequency | Key Variables | Access Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **[INDIA-APY](https://data.gov.in/resource/crop-production-statistics)** | Directorate of Economics & Statistics (DES) / data.gov.in | India (700+ Districts), 1997–2022 (Seasonal) | State, District, Crop Year, Season, Crop, Area (ha), Production (tonnes) | REST API / Bulk OGD CSV |
| **[AGMARKNET](https://agmarknet.gov.in/)** | DMI, Ministry of Agriculture & Farmers Welfare, GoI | India (3,200+ APMC Mandis), 2001–Present (Daily) | Market, Commodity, Variety, Arrival Date, Min/Max/Modal Price (INR/q) | OGD API / Portal Export |
| **[DES-AGR](https://desagri.gov.in/)** | Directorate of Economics & Statistics, GoI | India (National & State), 1950–Present (Annual) | Minimum Support Price (MSP), Land Use, Cost of Cultivation | Official Publications / XLSX |
| **[FAOSTAT-QCL](https://www.fao.org/faostat/en/#data/QCL)** | FAO of the United Nations | Global (245 Countries), 1961–Present (Annual) | Area harvested, Production volume, Yield, Commodity items | FAOSTAT REST API / Bulk CSV |
| **[WORLD-BANK-WDI](https://data.worldbank.org/indicator)** | The World Bank Group | Global (217 Economies), 1960–Present (Annual) | Cereal yield (kg/ha), Ag land (% of land), Ag value added (% of GDP) | World Bank API v2 / JSON |
| **[USDA-PSD](https://apps.fas.usda.gov/psdonline/)** | USDA Foreign Agricultural Service | Global Commodity Level, 1960–Present (Annual) | Beginning stocks, Production, Consumption, Trade, Ending stocks | USDA FAS CSV Bulk Export |

---

## 5. Key Metrics and KPIs

The analytical modules calculate twelve core agribusiness performance indicators:

1. **Crop Production ($P$)**: Aggregate volume harvested (Metric Tonnes).
2. **Crop Yield ($Y$)**: Land productivity efficiency: $Y = \frac{P \times 1000}{A}$ (kg/ha).
3. **Cultivated Area ($A$)**: Surface area under cultivation (Hectares).
4. **Production Growth Rate**: Year-over-Year (YoY) percentage change and Compound Annual Growth Rate (CAGR).
5. **Yield Growth Rate**: Intensive productivity change rate over time (% YoY).
6. **Commodity Modal Price**: Volume-weighted clearing price in APMC mandis (INR / Quintal).
7. **Price Volatility ($\sigma_{\text{returns}}$)**: Annualized standard deviation of logarithmic price returns.
8. **YoY Price Change**: Inflation-adjusted annual price comparison for identical calendar periods.
9. **Spatial Yield Index (SYI)**: Relative district productivity compared against national benchmark: $SYI = \left(\frac{Y_{\text{district}}}{\bar{Y}_{\text{national}}}\right) \times 100$.
10. **Cropping Intensity Index (CII)**: Land utilization ratio: $CII = \left(\frac{\text{Gross Cropped Area}}{\text{Net Sown Area}}\right) \times 100\%$.
11. **Seasonal Price Index (SPI)**: Standardized ratio of monthly prices relative to the annual trend.
12. **Arrival Elasticity of Price ($\varepsilon_a$)**: Sensitivity of wholesale price to harvest arrival surges.

---

## 6. Analytical Methodology

```
+---------------------------------------------------------------------------------------------------+
|                                   Methodological Workflow                                         |
+---------------------------------------------------------------------------------------------------+
| 1. Data Ingestion    -> Automated API queries, schema verification, SHA-256 manifest logging      |
| 2. Preprocessing     -> Entity resolution, taxonomic standardization, IQR & biological bounds     |
| 3. Exploratory EDA   -> Distributions, bivariate regressions, spatial yield choropleths, heatmap  |
| 4. Econometrics      -> ANOVA spatial tests, ADF unit root stationarity, STL seasonal decomposition|
| 5. Predictive Models -> Baseline (Naïve/MA), ARIMA/SARIMA, Random Forest/XGBoost Regressors       |
| 6. Validation        -> Temporal walk-forward cross-validation (MAE, RMSE, MAPE, sMAPE)           |
+---------------------------------------------------------------------------------------------------+
```

---

## 7. Repository Structure

```
agribusiness-data-analysis/
│
├── README.md                                 # Primary repository guide & executive overview
├── requirements.txt                          # Pinned project dependencies
├── .gitignore                                # Excludes bytecode, envs, and large raw data files
│
├── data/
│   ├── README.md                             # Data dictionary, schemas, and source protocols
│   ├── raw/                                  # Immutable raw data snapshots (ignored by git)
│   │   ├── .gitkeep
│   │   └── manifests/                        # Cryptographic audit logs & SHA-256 digests
│   └── processed/                            # Analysis-ready clean Parquet/CSV tables
│       └── .gitkeep
│
├── notebooks/
│   ├── 01_data_source_research.ipynb         # Data source survey, evaluation matrix & API tests
│   ├── 02_data_collection.ipynb              # Ingestion protocols, schema validation & logging
│   └── 03_initial_eda.ipynb                  # EDA framework, KPI demonstrations & styling
│
├── src/
│   ├── __init__.py                           # Package initialization
│   ├── utils.py                              # Logging, SHA-256 hashing, directory management
│   ├── data_collection.py                    # REST API collectors & schema validation inspectors
│   ├── data_cleaning.py                      # Outlier detection, unit conversion, taxonomic map
│   └── analysis.py                           # KPI calculators, econometric tests, forecast metrics
│
└── reports/
    └── week1_agribusiness_data_analysis_plan.md  # Comprehensive Week 1 planning report (20 sections)
```

---

## 8. Technology Stack

- **Core Programming**: [Python 3.10+](https://www.python.org/)
- **Data Wrangling & Pipeline**: [Pandas](https://pandas.pydata.org/) (v2.0+), [NumPy](https://numpy.org/) (v1.24+)
- **API & Data Transport**: [Requests](https://requests.readthedocs.io/), [OpenPyXL](https://openpyxl.readthedocs.io/), [PyArrow](https://arrow.apache.org/pyarrow/)
- **Statistical & Econometric Analysis**: [SciPy](https://scipy.org/), [Statsmodels](https://www.statsmodels.org/) (v0.14+), [Scikit-Learn](https://scikit-learn.org/) (v1.3+)
- **Visual Analytics**: [Matplotlib](https://matplotlib.org/) (v3.7+), [Seaborn](https://seaborn.pydata.org/) (v0.12+)
- **Interactive Environment**: [Jupyter Notebook](https://jupyter.org/)

---

## 9. Six-Week Project Roadmap

| Phase | Duration | Scope & Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Week 1** | Days 1–7 | **Research, Data Sourcing & Analytical Planning**: Candidate source catalog, KPI definitions, repository scaffolding, Week 1 report. | **COMPLETED** |
| **Week 2** | Days 8–14 | **Data Acquisition, Profiling & Preprocessing**: API downloads, deduplication, crop taxonomy mapping, biological outlier filtering. | *Upcoming* |
| **Week 3** | Days 15–21 | **Exploratory Data Analysis & Statistical Testing**: Spatial productivity choropleths, ANOVA yield tests, ADF stationarity, STL decomposition. | *Scheduled* |
| **Week 4** | Days 22–28 | **Econometric & ML Forecasting**: Implementation of Naïve, SARIMA, and XGBoost models; feature engineering of rolling windows and lags. | *Scheduled* |
| **Week 5** | Days 29–35 | **Model Evaluation & Residual Diagnostics**: Temporal walk-forward cross-validation, MAE/RMSE/MAPE error benchmarking, sensitivity analysis. | *Scheduled* |
| **Week 6** | Days 36–42 | **Final Synthesis, Interactive Dashboard & Defense**: Compilation of comprehensive final technical report, interactive dashboard, project defense. | *Scheduled* |

---

## 10. How to Reproduce the Work

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/agribusiness-data-analysis.git
   cd agribusiness-data-analysis
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Modular Package Installation**:
   ```bash
   python -c "import src; print('Package imported successfully!')"
   ```

5. **Launch Jupyter Notebooks**:
   ```bash
   jupyter notebook notebooks/
   ```
   Execute notebooks in numbered sequence (`01` $\rightarrow$ `02` $\rightarrow$ `03`).

---

## 11. Current Project Status

- [x] **Week 1 Planning Deliverable Completed**:
  - Full research survey across official agribusiness data sources (DES, Agmarknet, FAOSTAT, World Bank, USDA).
  - Formulation of 8 business research questions and 12 quantitative KPIs.
  - Development of modular Python modules in `src/` (`utils.py`, `data_collection.py`, `data_cleaning.py`, `analysis.py`).
  - Production of Jupyter starter notebooks in `notebooks/`.
  - Comprehensive Week 1 Report published in [`reports/week1_agribusiness_data_analysis_plan.md`](file:///c:/Users/bhowm/OneDrive/Documents/GitHub/agribusiness-market-analytics/reports/week1_agribusiness_data_analysis_plan.md).
- [ ] **Week 2 Execution Phase**: Ingestion of raw production and mandi price series scheduled next.

---

## 12. References & Attributions

- Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers Welfare, GoI: `https://desagri.gov.in/`
- Agmarknet Agricultural Marketing Information Network: `https://agmarknet.gov.in/`
- Open Government Data (OGD) Platform India: `https://data.gov.in/`
- Food and Agriculture Organization (FAO) Statistical Database: `https://www.fao.org/faostat/`
- World Bank Open Data: `https://data.worldbank.org/`
