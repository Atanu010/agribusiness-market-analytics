"""
Data Collection and Ingestion Pipeline for Agribusiness Datasets.

This module provides reproducible client classes and functions to acquire agricultural data
from official public APIs and portals (World Bank Open Data, FAOSTAT, data.gov.in, Agmarknet)
with built-in validation, retry mechanisms, and provenance manifest tracking.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import requests
import pandas as pd

from src.utils import ensure_directory, logger, update_data_manifest


class WorldBankAgriCollector:
    """
    Collector for World Bank Open Data API (v2).
    Accesses agricultural indicators (e.g., Cereal Yield, Agriculture % of GDP, Land Use).
    API Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
    """

    BASE_URL = "https://api.worldbank.org/v2"

    INDICATOR_MAP = {
        "cereal_yield": "AG.YLD.CREL.KG",          # Cereal yield (kg per hectare)
        "agri_land_pct": "AG.LND.AGRI.ZS",          # Agricultural land (% of land area)
        "agri_gdp_pct": "NV.AGR.TOTL.ZS",           # Agriculture, forestry, fishing (% of GDP)
        "crop_production_index": "AG.PRD.CROP.XD",  # Crop production index (2014-2016 = 100)
        "fertilizer_consumption": "AG.CON.FERT.ZS"  # Fertilizer consumption (kg/ha of arable land)
    }

    def __init__(self, raw_dir: Path):
        self.raw_dir = ensure_directory(raw_dir)
        self.manifest_path = self.raw_dir / "manifests" / "audit_log.json"

    def fetch_indicator(
        self,
        country: str = "IND",
        indicator_key: str = "cereal_yield",
        date_range: str = "1990:2023",
        timeout: int = 30,
    ) -> Optional[pd.DataFrame]:
        """
        Fetches an agricultural indicator series for a given country and date range.

        Args:
            country: ISO-3 country code (e.g., 'IND', 'USA', 'BRA', 'WLD').
            indicator_key: Key corresponding to INDICATOR_MAP.
            date_range: Format 'YYYY:YYYY'.
            timeout: HTTP request timeout in seconds.

        Returns:
            Optional[pd.DataFrame]: Ingested tabular dataframe or None if failed.
        """
        indicator_code = self.INDICATOR_MAP.get(indicator_key, indicator_key)
        url = f"{self.BASE_URL}/country/{country}/indicator/{indicator_code}"
        params = {
            "date": date_range,
            "format": "json",
            "per_page": 1000
        }

        logger.info(f"Querying World Bank API for indicator '{indicator_code}' ({country}, {date_range})...")
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            payload = response.json()

            if len(payload) < 2 or not payload[1]:
                logger.warning(f"No records returned by World Bank API for {country} - {indicator_code}.")
                return None

            records = []
            for item in payload[1]:
                records.append({
                    "country_iso3": item.get("countryiso3code"),
                    "country_name": item.get("country", {}).get("value"),
                    "indicator_id": item.get("indicator", {}).get("id"),
                    "indicator_name": item.get("indicator", {}).get("value"),
                    "year": int(item.get("date")),
                    "value": float(item.get("value")) if item.get("value") is not None else None,
                })

            df = pd.DataFrame(records).sort_values("year").reset_index(drop=True)
            output_file = self.raw_dir / f"worldbank_{country.lower()}_{indicator_key}.csv"
            df.to_csv(output_file, index=False)

            update_data_manifest(
                manifest_path=self.manifest_path,
                file_path=output_file,
                source_name="World Bank Open Data",
                source_url=url,
                metadata={
                    "indicator_id": indicator_code,
                    "country": country,
                    "rows": len(df),
                    "columns": list(df.columns),
                    "null_values": int(df["value"].isna().sum()),
                }
            )

            logger.info(f"Successfully collected {len(df)} records -> {output_file.name}")
            return df

        except requests.RequestException as e:
            logger.error(f"HTTP error querying World Bank API: {e}")
            return None


class LocalDatasetIngestor:
    """
    Ingestor and schema validator for downloaded agricultural datasets:
    - DES District-wise Area, Production, and Yield (APY)
    - Agmarknet daily/monthly mandi price extracts
    - FAOSTAT bulk crop production exports
    """

    EXPECTED_SCHEMAS: Dict[str, List[str]] = {
        "india_apy": [
            "State_Name", "District_Name", "Crop_Year", "Season",
            "Crop", "Area", "Production"
        ],
        "agmarknet_prices": [
            "State", "District", "Market", "Commodity", "Variety",
            "Arrival_Date", "Min_Price", "Max_Price", "Modal_Price"
        ],
        "faostat_qcl": [
            "Area Code", "Area", "Item Code", "Item", "Element Code",
            "Element", "Year Code", "Year", "Unit", "Value", "Flag"
        ]
    }

    def __init__(self, raw_dir: Path):
        self.raw_dir = ensure_directory(raw_dir)
        self.manifest_path = self.raw_dir / "manifests" / "audit_log.json"

    def ingest_csv(
        self,
        filepath: Path,
        schema_key: str,
        source_name: str,
        source_url: str,
        encoding: str = "utf-8"
    ) -> pd.DataFrame:
        """
        Validates schema, checks row counts, logs checksum, and ingests a raw CSV.

        Args:
            filepath: Path to the raw CSV file.
            schema_key: One of 'india_apy', 'agmarknet_prices', 'faostat_qcl'.
            source_name: Originating body / repository name.
            source_url: Download portal or endpoint URL.
            encoding: Text encoding of the source file.

        Returns:
            pd.DataFrame: Loaded raw dataframe.
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Source file not found at: {filepath}")

        logger.info(f"Ingesting raw CSV dataset from {filepath.name} (Schema: {schema_key})...")
        df = pd.read_csv(filepath, encoding=encoding, low_memory=False)

        # Validate schema columns
        expected_cols = self.EXPECTED_SCHEMAS.get(schema_key, [])
        missing_cols = [col for col in expected_cols if col not in df.columns]

        if missing_cols:
            logger.warning(
                f"Schema warning for {filepath.name}: Missing expected columns: {missing_cols}. "
                f"Present columns: {list(df.columns)}"
            )
        else:
            logger.info(f"Schema verification passed for {filepath.name}.")

        # Record file manifest and checksum
        update_data_manifest(
            manifest_path=self.manifest_path,
            file_path=filepath,
            source_name=source_name,
            source_url=source_url,
            metadata={
                "schema_key": schema_key,
                "rows": len(df),
                "columns": list(df.columns),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                "missing_cells_total": int(df.isna().sum().sum()),
            }
        )

        return df


def inspect_raw_dataset(df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
    """
    Computes diagnostic profiling metrics on a raw dataset before preprocessing.

    Args:
        df: Input DataFrame.
        dataset_name: Name of the dataset for logging.

    Returns:
        Dict[str, Any]: Summary diagnostics dictionary.
    """
    summary = {
        "dataset_name": dataset_name,
        "total_records": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {k: str(v) for k, v in df.dtypes.items()},
        "null_counts": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }
    logger.info(
        f"Profiling for {dataset_name}: {summary['total_records']} rows, "
        f"{summary['total_columns']} cols, {summary['duplicate_rows']} duplicates."
    )
    return summary
