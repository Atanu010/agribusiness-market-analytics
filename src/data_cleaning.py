"""
Data Cleaning, Normalization, and Preprocessing Module for Agribusiness Datasets.

This module provides reproducible transformation functions to clean and harmonize
agricultural panel data (APY) and commodity price time-series (Agmarknet).
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from src.utils import ensure_directory, logger


# Canonical Crop Category Mapping
CROP_CATEGORY_MAP: Dict[str, str] = {
    "Rice": "Cereals",
    "Paddy": "Cereals",
    "Wheat": "Cereals",
    "Maize": "Cereals",
    "Jowar": "Cereals",
    "Bajra": "Cereals",
    "Barley": "Cereals",
    "Ragi": "Cereals",
    "Gram": "Pulses",
    "Chickpea": "Pulses",
    "Arhar/Tur": "Pulses",
    "Pigeonpea": "Pulses",
    "Moong(Green Gram)": "Pulses",
    "Urad": "Pulses",
    "Lentil": "Pulses",
    "Masur": "Pulses",
    "Groundnut": "Oilseeds",
    "Soyabean": "Oilseeds",
    "Rapeseed &Mustard": "Oilseeds",
    "Mustard": "Oilseeds",
    "Sunflower": "Oilseeds",
    "Sesamum": "Oilseeds",
    "Cotton(lint)": "Commercial",
    "Sugarcane": "Commercial",
    "Jute": "Commercial",
    "Tobacco": "Commercial",
    "Potato": "Horticulture",
    "Onion": "Horticulture",
    "Tomato": "Horticulture",
}

# State Name Normalization
STATE_NAME_MAPPINGS: Dict[str, str] = {
    "Orissa": "Odisha",
    "Uttaranchal": "Uttarakhand",
    "Pondicherry": "Puducherry",
    "Andaman and Nicobar Islands": "Andaman and Nicobar",
    "Jammu and Kashmir ": "Jammu and Kashmir",
}

# Physical plausible yield thresholds (kg/ha) for anomaly detection
YIELD_PHYSICAL_BOUNDS: Dict[str, Tuple[float, float]] = {
    "Cereals": (100.0, 15000.0),      # Minimum 100 kg/ha, max 15,000 kg/ha (15 t/ha)
    "Pulses": (50.0, 4500.0),         # Pulses yield rarely exceeds 4.5 t/ha
    "Oilseeds": (50.0, 6000.0),       # High-oil varieties cap ~5-6 t/ha
    "Commercial": (200.0, 150000.0),  # Sugarcane green cane biomass can reach 120-140 t/ha
    "Horticulture": (500.0, 60000.0), # Tuber crops (potato) up to 50-60 t/ha
}


class APYDataCleaner:
    """
    Cleans, standardizes, and validates Area, Production, and Yield (APY) datasets.
    """

    def __init__(self, raw_df: pd.DataFrame):
        self.df = raw_df.copy()
        self.audit_trail: List[str] = []

    def clean_column_names(self) -> "APYDataCleaner":
        """Strips whitespace and standardizes column names to snake_case."""
        initial_cols = list(self.df.columns)
        self.df.columns = (
            self.df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        self.audit_trail.append(f"Standardized columns: {initial_cols} -> {list(self.df.columns)}")
        return self

    def standardize_entities(self) -> "APYDataCleaner":
        """Normalizes state, district, crop names, and seasons."""
        # Clean text columns
        for col in ["state_name", "district_name", "crop", "season"]:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.title()

        # Map legacy state names
        if "state_name" in self.df.columns:
            self.df["state_name"] = self.df["state_name"].replace(STATE_NAME_MAPPINGS)

        # Standardize crop names
        if "crop" in self.df.columns:
            # Map Paddy to Rice
            self.df["crop"] = self.df["crop"].replace({"Paddy": "Rice", "Gram": "Chickpea"})
            # Assign crop category
            self.df["crop_category"] = self.df["crop"].map(CROP_CATEGORY_MAP).fillna("Other")

        # Standardize seasons
        if "season" in self.df.columns:
            self.df["season"] = self.df["season"].str.replace(r"\s+", " ", regex=True).str.strip()

        self.audit_trail.append("Applied entity name normalization and crop category categorization.")
        return self

    def handle_duplicates_and_nulls(self) -> "APYDataCleaner":
        """
        Removes identical duplicate entries and handles missing numeric fields.
        """
        initial_len = len(self.df)

        # Check composite primary key
        key_cols = [c for c in ["state_name", "district_name", "crop_year", "season", "crop"] if c in self.df.columns]
        if key_cols:
            self.df = self.df.drop_duplicates(subset=key_cols, keep="first")
            dupes_removed = initial_len - len(self.df)
            self.audit_trail.append(f"Removed {dupes_removed} duplicate records on key {key_cols}.")

        # Handle missing Area or Production
        # If both are null or zero, record is uninformative
        if "area" in self.df.columns and "production" in self.df.columns:
            self.df["area"] = pd.to_numeric(self.df["area"], errors="coerce")
            self.df["production"] = pd.to_numeric(self.df["production"], errors="coerce")

            valid_mask = (self.df["area"] > 0) & (self.df["production"].notna())
            dropped_rows = len(self.df) - valid_mask.sum()
            self.df = self.df[valid_mask].copy()
            self.audit_trail.append(f"Filtered out {dropped_rows} records with invalid/missing Area or Production.")

        return self

    def calculate_yield(self) -> "APYDataCleaner":
        """
        Computes crop yield in kg/hectare.
        Formula: Yield (kg/ha) = (Production in Metric Tonnes * 1000) / Area in Hectares
        """
        if "area" in self.df.columns and "production" in self.df.columns:
            # Area in Hectares, Production in Tonnes -> Yield in kg/ha
            self.df["yield_kg_per_ha"] = (self.df["production"] * 1000.0) / self.df["area"]
            self.df["yield_tonnes_per_ha"] = self.df["production"] / self.df["area"]
            self.audit_trail.append("Computed yield_kg_per_ha and yield_tonnes_per_ha.")
        return self

    def flag_outliers(self, iqr_multiplier: float = 3.0) -> "APYDataCleaner":
        """
        Identifies and flags extreme yield outliers using domain-specific bounds and IQR.
        Outliers are flagged in a boolean column 'is_outlier' rather than silently dropped.
        """
        self.df["is_outlier"] = False
        self.df["outlier_reason"] = "Valid"

        if "yield_kg_per_ha" not in self.df.columns:
            return self

        # 1. Biological bound checks
        for cat, (lower_b, upper_b) in YIELD_PHYSICAL_BOUNDS.items():
            cat_mask = self.df.get("crop_category", "") == cat
            viol_mask = cat_mask & ((self.df["yield_kg_per_ha"] < lower_b) | (self.df["yield_kg_per_ha"] > upper_b))
            self.df.loc[viol_mask, "is_outlier"] = True
            self.df.loc[viol_mask, "outlier_reason"] = f"Exceeds physical biological bound for {cat}"

        # 2. IQR outlier detection grouped by crop
        for crop, group in self.df.groupby("crop"):
            if len(group) < 30:
                continue
            q25 = group["yield_kg_per_ha"].quantile(0.25)
            q75 = group["yield_kg_per_ha"].quantile(0.75)
            iqr = q75 - q25
            if iqr > 0:
                upper_fence = q75 + (iqr_multiplier * iqr)
                lower_fence = max(0.0, q25 - (iqr_multiplier * iqr))
                crop_idx = group[
                    (group["yield_kg_per_ha"] > upper_fence) | (group["yield_kg_per_ha"] < lower_fence)
                ].index
                self.df.loc[crop_idx, "is_outlier"] = True
                self.df.loc[crop_idx, "outlier_reason"] = "Statistical IQR anomaly"

        total_flagged = int(self.df["is_outlier"].sum())
        self.audit_trail.append(f"Flagged {total_flagged} records as yield anomalies/outliers.")
        return self

    def get_clean_data(self) -> pd.DataFrame:
        """Returns the processed DataFrame and logs audit summary."""
        for step in self.audit_trail:
            logger.info(f"[APY Cleaner] {step}")
        return self.df.reset_index(drop=True)


class MandiPriceCleaner:
    """
    Cleans and standardizes Agmarknet wholesale agricultural commodity price data.
    """

    def __init__(self, raw_df: pd.DataFrame):
        self.df = raw_df.copy()
        self.audit_trail: List[str] = []

    def clean_and_validate(self) -> pd.DataFrame:
        """
        Executes standard parsing and validation pipeline on mandi price series.
        """
        self.df.columns = (
            self.df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # Standardize date
        date_col = next((c for c in ["arrival_date", "date"] if c in self.df.columns), None)
        if date_col:
            self.df["date"] = pd.to_datetime(self.df[date_col], errors="coerce")
            self.df = self.df[self.df["date"].notna()].copy()
            self.df["year"] = self.df["date"].dt.year
            self.df["month"] = self.df["date"].dt.month
            self.df["quarter"] = self.df["date"].dt.quarter
            self.audit_trail.append("Parsed ISO date and generated calendar attributes.")

        # Numeric price coercion
        price_cols = [c for c in ["min_price", "max_price", "modal_price"] if c in self.df.columns]
        for p_col in price_cols:
            self.df[p_col] = pd.to_numeric(
                self.df[p_col].astype(str).str.replace(",", "").str.strip(),
                errors="coerce"
            )

        # Logical price validation: Min_Price <= Modal_Price <= Max_Price & Price > 0
        if "modal_price" in self.df.columns:
            valid_price = self.df["modal_price"] > 0
            self.df = self.df[valid_price].copy()
            self.audit_trail.append(f"Filtered invalid zero/negative modal prices. Remaining: {len(self.df)}")

        for step in self.audit_trail:
            logger.info(f"[Mandi Price Cleaner] {step}")

        return self.df.reset_index(drop=True)
