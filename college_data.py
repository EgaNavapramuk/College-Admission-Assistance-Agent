from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd

Gender = Literal["BOYS", "GIRLS"]


@dataclass(frozen=True)
class CollegeDataset:
    df: pd.DataFrame
    cutoff_columns: dict[tuple[str, Gender], str]


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize `cleaned.xlsx` columns into stable, code-friendly names.
    """
    rename_map: dict[str, str] = {
        "INSTITUTE CODE": "Institute_Code",
        "INSTITUTE NAME": "Institute_Name",
        "DISTRICT": "District",
        "CO_EDUCATION": "Co_Education",
        "COLLEGE TYPE": "College_Type",
        "BRANCH CODE": "Branch_Code",
        "BRANCH NAME": "Branch_Name",
        "FEE": "Fee",
        # Diploma-style headers with newlines
        "OC \nBOYS": "OC_BOYS",
        "OC \nGIRLS": "OC_GIRLS",
        "BC_A \nBOYS": "BC_A_BOYS",
        "BC_A \nGIRLS": "BC_A_GIRLS",
        "BC_B \nBOYS": "BC_B_BOYS",
        "BC_B \nGIRLS": "BC_B_GIRLS",
        "BC_C \nBOYS": "BC_C_BOYS",
        "BC_C \nGIRLS": "BC_C_GIRLS",
        "BC_D \nBOYS": "BC_D_BOYS",
        "BC_D \nGIRLS": "BC_D_GIRLS",
        "BC_E \nBOYS": "BC_E_BOYS",
        "BC_E \nGIRLS": "BC_E_GIRLS",
        "SC \nBOYS": "SC_BOYS",
        "SC \nGIRLS": "SC_GIRLS",
        "ST \nBOYS": "ST_BOYS",
        "ST \nGIRLS": "ST_GIRLS",
        "EWS \nGEN OU": "EWS_BOYS",
        "EWS \nGIRLS OU": "EWS_GIRLS",
        # Engineering/Medical-style headers with spaces instead of newlines
        "OC BOYS": "OC_BOYS",
        "OC GIRLS": "OC_GIRLS",
        "BC_A BOYS": "BC_A_BOYS",
        "BC_A GIRLS": "BC_A_GIRLS",
        "BC_B BOYS": "BC_B_BOYS",
        "BC_B GIRLS": "BC_B_GIRLS",
        "BC_C BOYS": "BC_C_BOYS",
        "BC_C GIRLS": "BC_C_GIRLS",
        "BC_D BOYS": "BC_D_BOYS",
        "BC_D GIRLS": "BC_D_GIRLS",
        "BC_E BOYS": "BC_E_BOYS",
        "BC_E GIRLS": "BC_E_GIRLS",
        "SC BOYS": "SC_BOYS",
        "SC GIRLS": "SC_GIRLS",
        "ST BOYS": "ST_BOYS",
        "ST GIRLS": "ST_GIRLS",
        "EWS GEN OU": "EWS_BOYS",
        "EWS GIRLS OU": "EWS_GIRLS",
    }

    # Some Excel exports have extra spaces or different newlines; normalize keys.
    normalized_map: dict[str, str] = {
        str(k).replace("\r\n", "\n").replace("\r", "\n").strip(): v
        for k, v in rename_map.items()
    }
    df = df.rename(
        columns={
            str(c).replace("\r\n", "\n").replace("\r", "\n").strip(): normalized_map.get(
                str(c).replace("\r\n", "\n").replace("\r", "\n").strip(), c
            )
            for c in df.columns
        }
    )

    # Fallbacks for slightly different or friendlier column names that may appear
    # in other datasets (Engineering / Medical variants, etc.).
    fallback_variants: dict[str, list[str]] = {
        "Institute_Name": ["Institute Name", "INSTITUTE", "Institute"],
        "Branch_Name": ["Branch Name", "BRANCH", "Branch"],
        "Fee": ["Fee", "FEES", "TUITION FEE", "Tuition Fee"],
    }
    for canonical, candidates in fallback_variants.items():
        if canonical in df.columns:
            continue
        for cand in candidates:
            if cand in df.columns:
                df = df.rename(columns={cand: canonical})
                break

    return df


def load_college_dataset(path: str | Path = "cleaned.xlsx") -> CollegeDataset:
    path = Path(path)
    df = pd.read_excel(path).copy()
    df = _rename_columns(df)

    # Only drop rows on columns that actually exist in this file to avoid KeyError
    required = ["Institute_Name", "Branch_Name", "Fee"]
    existing_required = [c for c in required if c in df.columns]
    if existing_required:
        df = df.dropna(subset=existing_required)

    # Enforce dtypes
    if "Institute_Name" in df.columns:
        df["Institute_Name"] = df["Institute_Name"].astype(str).str.strip()
    if "Branch_Name" in df.columns:
        df["Branch_Name"] = df["Branch_Name"].astype(str).str.strip()
    df["District"] = df.get("District", "").astype(str).str.strip()
    df["Fee"] = pd.to_numeric(df["Fee"], errors="coerce")

    cutoff_columns: dict[tuple[str, Gender], str] = {}
    for col in df.columns:
        if not isinstance(col, str):
            continue
        if col.endswith("_BOYS"):
            cutoff_columns[(col.removesuffix("_BOYS"), "BOYS")] = col
        elif col.endswith("_GIRLS"):
            cutoff_columns[(col.removesuffix("_GIRLS"), "GIRLS")] = col

    return CollegeDataset(df=df, cutoff_columns=cutoff_columns)


def available_categories(dataset: CollegeDataset) -> list[str]:
    cats = sorted({cat for (cat, _gender) in dataset.cutoff_columns.keys()})
    return cats


def available_branches(dataset: CollegeDataset) -> list[str]:
    return sorted(dataset.df["Branch_Name"].dropna().astype(str).str.strip().unique().tolist())


def available_districts(dataset: CollegeDataset) -> list[str]:
    if "District" not in dataset.df.columns:
        return []
    vals = dataset.df["District"].dropna().astype(str).str.strip()
    return sorted({v for v in vals.tolist() if v})


def cutoff_column(dataset: CollegeDataset, category: str, gender: Gender) -> str | None:
    key = (category.strip().upper(), gender)
    # categories are stored as upper tokens (OC, SC, BC_A, ...)
    for (cat, gen), col in dataset.cutoff_columns.items():
        if cat.upper() == key[0] and gen == gender:
            return col
    return None