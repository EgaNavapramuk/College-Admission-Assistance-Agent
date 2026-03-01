import pandas as pd

df = pd.read_csv("data/master_college_data_updated.csv")

def recommend_colleges(student_rank, budget=None, state=None):

    eligible = df[
        (df["opening_rank"] <= student_rank) &
        (df["closing_rank"] >= student_rank)
    ].copy()

    if budget:
        eligible = eligible[eligible["estimated_fees"] <= budget]

    if state:
        eligible = eligible[eligible["state"].str.lower() == state.lower()]

    if eligible.empty:
        return None

    eligible["rank_fit"] = (
        (eligible["closing_rank"] - student_rank) /
        (eligible["closing_rank"] - eligible["opening_rank"] + 1)
    )

    eligible["nirf_score_norm"] = 1 / eligible["nirf_rank"]

    eligible["final_score"] = (
        0.6 * eligible["rank_fit"] +
        0.4 * eligible["nirf_score_norm"]
    )

    return eligible.sort_values("final_score", ascending=False)