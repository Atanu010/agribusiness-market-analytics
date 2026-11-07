# Agribusiness Data Management & Architecture Guide

## 1. Overview and Purpose

This directory manages all input, intermediate, and analysis-ready datasets for the **Agribusiness Data Analysis and Forecasting** project. In accordance with enterprise data engineering standards and scientific reproducibility guidelines:

- **Raw data (`data/raw/`)** is strictly **immutable** and treated as read-only.
- **Processed data (`data/processed/`)** contains standardized, validated, and feature-engineered analytical tables.
- **Version tracking and metadata manifests** ensure complete provenance from source endpoint to final model input.

> **Project Phase Notice**: As of **Week 1 (Planning Phase)**, this directory documents schemas, source acquisition protocols, and data dictionary contracts. Full dataset ingestion and batch cleaning runs are scheduled for **Week 2**.

---

## 2. Directory Hierarchy

```
data/
├── raw/                      # Unaltered source extracts (CSV, JSON, XLSX)
│   ├── .gitkeep              # Git tracking anchor
│   └── manifests/            # Ingestion logs, SHA-256 hashes, timestamps
│
├── processed/                # Analysis-ready datasets (Parquet, CSV)
│   ├── .gitkeep              # Git tracking anchor
│   ├── crop_apy_clean.parquet# Harmonized Area-Production-Yield panel
│   └── mandi_prices_clean.parquet # Cleaned daily/monthly commodity prices
│
└── README.md                 # Data documentation and source acquisition guide
```

---

## 3. Data Storage and Immutability Policy

1. **Read-Only Raw Zone**: Files placed in `data/raw/` must never be manually edited, reformatted, or overwritten. If an API query or manual download is updated, a timestamped snapshot is saved (e.g., `agmarknet_wheat_20261107.csv`).
2. **Deterministic Processing**: Any table in `data/processed/` must be completely reproducible by executing the collection and cleaning scripts in `src/`.
3. **Storage Format**: Large analytical panels are stored in Apache Parquet (`.parquet`) for columnar compression and fast read access, alongside CSV counterparts for auditing.
4. **Git Policy**: Raw and large processed datasets (`> 1 MB`) are excluded from Git tracking via `.gitignore` to prevent repository bloat and comply with data redistribution licenses.

---

## 4. Primary Data Sources & Acquisition Protocols

| Source Identifier | Host Organization | Coverage | Primary Variables | Access Method | Planned Target File |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **APY-INDIA** | Directorate of Economics & Statistics (DES) / data.gov.in | India (State/District level), 1997–2021+ | State, District, Crop, Crop Year, Season, Area (ha), Production (tonnes), Yield (kg/ha) | REST API / OGD CSV Export | `data/raw/apy_district_india.csv` |
| **AGMARKNET** | DMI, Ministry of Agriculture & Farmers Welfare | India (APMC Mandis), 2015–Present | State, District, Market, Commodity, Variety, Arrival Date, Min Price, Max Price, Modal Price (INR/Quintal) | Web Portal / Custom Scraper / API | `data/raw/agmarknet_modal_prices.csv` |
| **FAOSTAT-QCL** | Food and Agriculture Organization (FAO), UN | Global (200+ countries), 1961–2022+ | Country, Element (Area harvested, Production, Yield), Item (Crops), Year, Unit, Value | FAOSTAT API / Bulk Download | `data/raw/faostat_qcl_production.csv` |
| **WORLD-BANK-WDI** | World Bank Open Data | Global, 1960–Present | Agricultural land (% of land area), Cereal yield (kg/ha), Ag value added (% of GDP) | World Bank Indicators API (`api.worldbank.org/v2`) | `data/raw/worldbank_agri_indicators.json` |
| **USDA-PSD** | USDA Foreign Agricultural Service (FAS) | Global Commodity Level, 1960–Present | Commodity, Country, Market Year, Beginning Stocks, Production, Imports, Exports, Ending Stocks | USDA FAS PSD Online CSV Export | `data/raw/usda_psd_grains_oilseeds.csv` |

---

## 5. Standardized Data Dictionary & Units

To prevent discrepancies during cross-source merging, the following standardization rules will be enforced during the Week 2 cleaning pipeline:

| Dimension / Metric | Standard Unit | Source Variants Encountered | Conversion Formula |
| :--- | :--- | :--- | :--- |
| **Cultivated Area** | **Hectare (ha)** | Acres, Bigha, Hectares, Thousand Hectares | $1\text{ ha} = 2.47105\text{ acres}$; Thousand Ha $\times 1000$ |
| **Crop Production** | **Metric Tonne (t)** | Quintals, Kilograms, Tonnes, Metric Tons, Bushels | $1\text{ Tonne} = 10\text{ Quintals} = 1,000\text{ kg}$ |
| **Crop Yield** | **Kilograms / Hectare (kg/ha)** | Tonnes/ha, Quintals/acre, kg/ha, Bushels/acre | $\text{kg/ha} = \frac{\text{Production (t)} \times 1000}{\text{Area (ha)}}$ |
| **Wholesale Price** | **INR / Quintal (INR/q)** | INR/kg, INR/tonne, USD/Metric Tonne | $\text{INR/q} = \text{INR/kg} \times 100 = \frac{\text{INR/tonne}}{10}$ |
| **Time Format** | **ISO 8601 (`YYYY-MM-DD`)** | `DD/MM/YYYY`, `MM-DD-YYYY`, `YYYY-YY` | Converted via `pd.to_datetime()` |
| **Crop Season** | **Standard Categories** | Kharif, Rabi, Summer/Zaid, Autumn, Winter, Annual | Mapped via canonical seasonal ontology dictionary |

---

## 6. Data Integrity & Verification Protocol

When files are downloaded into `data/raw/`:
1. Calculate and log the SHA-256 cryptographic checksum.
2. Record file size, row count, byte encoding, and timestamp in `data/raw/manifests/audit_log.json`.
3. Verify that zero byte files or truncated HTTP responses are caught prior to processing.
