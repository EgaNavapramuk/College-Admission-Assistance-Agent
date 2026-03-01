import pandas as pd

def classify_status(student_rank, closing_rank):
    ratio = student_rank / closing_rank
    if ratio <= 0.3:
        return "🔥 Dream"
    elif ratio <= 0.7:
        return "⚖ Moderate"
    else:
        return "✅ Safe"

def recommend_polytechnic(rank, category, branch=None, max_fee=None):

    df = pd.read_csv("data/polytechnic.csv")
    df.columns = df.columns.str.strip()

    # Find category column
    rank_column = None
    for col in df.columns:
        if category in col and "BOYS" in col:
            rank_column = col
            break

    if rank_column is None:
        return None

    df[rank_column] = pd.to_numeric(df[rank_column], errors="coerce")

    eligible = df[df[rank_column] >= rank].copy()

    if branch and branch != "All Branches":
        eligible = eligible[eligible["BRANCH NAME"] == branch]

    if max_fee and max_fee > 0:
        eligible = eligible[eligible["FEE"] <= max_fee]

    if eligible.empty:
        return None

    eligible["STATUS"] = eligible[rank_column].apply(
        lambda x: classify_status(rank, x)
    )

    return eligible[[
        "INSTITUTE NAME",
        "BRANCH NAME",
        "DISTRICT",
        "COLLEGE TYPE",
        "FEE",
        "STATUS"
    ]]