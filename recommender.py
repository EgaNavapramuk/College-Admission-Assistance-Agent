from __future__ import annotations

import pandas as pd

from college_data import Gender, cutoff_column, load_college_dataset


def _classify(rank: int, cutoff: float) -> str:
    if cutoff <= 0:
        return "Unknown"
    ratio = rank / cutoff
    if ratio <= 0.7:
        return "Dream"
    if ratio <= 1.0:
        return "Target"
    return "Safe"


def recommend(
    rank: int,
    category: str,
    gender: Gender,
    branch: str,
    budget: int,
    district_query: str,
    college_type: str = "(Any)",
    co_ed: str = "(Any)",
    top_k: int = 15,
    dataset_file: str = "cleaned.xlsx",
) -> pd.DataFrame:
    try:
        dataset = load_college_dataset(dataset_file)
    except FileNotFoundError:
        dataset = load_college_dataset("cleaned.xlsx") # fallback
        
    df = dataset.df.copy()

    cutoff_col = cutoff_column(dataset, category, gender)
    if not cutoff_col:
        return pd.DataFrame()

    df[cutoff_col] = pd.to_numeric(df[cutoff_col], errors="coerce")

    branch_norm = (branch or "").strip().upper()
    district_norm = (district_query or "").strip().upper()
    budget_val = int(budget or 0)

    filtered = df[df[cutoff_col].notna()].copy()
    filtered = filtered[filtered[cutoff_col] >= rank]

    if branch_norm:
        filtered = filtered[
            filtered["Branch_Name"].astype(str).str.upper().str.strip().str.contains(branch_norm, regex=False)
        ]

    if budget_val > 0:
        filtered = filtered[filtered["Fee"].notna() & (filtered["Fee"] <= budget_val)]

    if district_norm and "District" in filtered.columns:
        filtered = filtered[
            filtered["District"].astype(str).str.upper().str.contains(district_norm, regex=False)
        ]

    if college_type and college_type != "(Any)" and "College_Type" in filtered.columns:
        filtered = filtered[
            filtered["College_Type"].astype(str).str.upper().str.strip().eq(college_type.strip().upper())
        ]

    if co_ed and co_ed != "(Any)" and "Co_Education" in filtered.columns:
        filtered = filtered[
            filtered["Co_Education"].astype(str).str.upper().str.strip().eq(co_ed.strip().upper())
        ]

    if filtered.empty:
        return filtered

    # Scores
    # Rank score: higher is better (more margin between cutoff and student rank)
    filtered["Rank_Score"] = ((filtered[cutoff_col] - rank) / filtered[cutoff_col]).clip(lower=0.0, upper=1.0)

    if budget_val > 0:
        filtered["Fee_Score"] = (1.0 - (filtered["Fee"] / budget_val)).clip(lower=0.0, upper=1.0)
    else:
        filtered["Fee_Score"] = 0.5

    if district_norm and "District" in filtered.columns:
        district_exact = filtered["District"].astype(str).str.upper().str.strip().eq(district_norm)
        filtered["Location_Score"] = district_exact.astype(float)
    else:
        filtered["Location_Score"] = 0.0

    filtered["Score"] = (
        0.65 * filtered["Rank_Score"]
        + 0.25 * filtered["Fee_Score"]
        + 0.10 * filtered["Location_Score"]
    )

    filtered["Category_Type"] = filtered.apply(lambda r: _classify(rank, float(r[cutoff_col])), axis=1)
    filtered["Cutoff_Column"] = cutoff_col
    filtered["Cutoff_Rank"] = filtered[cutoff_col]

    show_cols = [
        "Institute_Name",
        "District",
        "Branch_Name",
        "Fee",
        "Cutoff_Rank",
        "Category_Type",
        "Score",
    ]
    # keep any missing columns safe
    show_cols = [c for c in show_cols if c in filtered.columns]
    out = filtered.sort_values(by="Score", ascending=False)
    out = out.head(int(top_k)).reset_index(drop=True)
    return out[show_cols + [c for c in out.columns if c not in show_cols]]