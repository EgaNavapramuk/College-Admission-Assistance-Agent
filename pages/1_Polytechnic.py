import streamlit as st
import pandas as pd
from polytechnic_engine import recommend_polytechnic

st.title("🎓 Polytechnic Explorer")

rank = st.number_input("Enter Rank", min_value=1)
category = st.selectbox("Category", ["OC", "BC_A", "BC_B", "SC", "ST"])

poly_df = pd.read_csv("data/polytechnic.csv")
branches = sorted(poly_df["BRANCH NAME"].dropna().unique())

branch = st.selectbox("Branch", ["All Branches"] + branches)
budget = st.number_input("Max Budget", min_value=0)

if st.button("Search Polytechnic"):
    results = recommend_polytechnic(rank, category, branch, budget)
    if results is None:
        st.warning("No results found")
    else:
        st.dataframe(results)