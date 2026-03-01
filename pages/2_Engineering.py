import streamlit as st
import pandas as pd

st.title("🏫 Engineering Colleges Finder")

# Load master engineering dataset
df = pd.read_csv("data/master_college_data_updated.csv")

rank = st.number_input("Enter JEE Rank", min_value=1)

sort_option = st.selectbox(
    "Sort By",
    ["Best NIRF Rank", "Low Opening Rank"]
)

if st.button("Search Engineering"):

    # Filter eligible colleges
    eligible = df[
        (df["opening_rank"] <= rank) &
        (df["closing_rank"] >= rank)
    ].copy()

    if eligible.empty:
        st.warning("No colleges found for this rank.")
    else:

        st.success(f"🎯 {len(eligible)} Colleges Found")

        # Sorting logic
        if sort_option == "Best NIRF Rank":
            eligible = eligible.sort_values("nirf_rank")
        else:
            eligible = eligible.sort_values("opening_rank")

        # Display cards
        for _, row in eligible.iterrows():
            st.markdown(f"""
            <div style="
                padding:20px;
                border-radius:12px;
                background:#1E1E1E;
                margin-bottom:15px;
                box-shadow:0px 5px 15px rgba(0,0,0,0.5);
            ">
                <h4>{row['college_name']}</h4>
                <p><b>NIRF Rank:</b> {row['nirf_rank']}</p>
                <p><b>Opening Rank:</b> {row['opening_rank']}</p>
                <p><b>Closing Rank:</b> {row['closing_rank']}</p>
            </div>
            """, unsafe_allow_html=True)