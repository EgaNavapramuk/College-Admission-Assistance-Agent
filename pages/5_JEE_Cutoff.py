import streamlit as st
import pandas as pd

st.title("📊 JEE Main Cutoff Explorer")

# Load dataset
df = pd.read_csv("data/jee_cutoff.csv")

# ================= INSTITUTE =================
institute = st.selectbox(
    "Select Institute",
    sorted(df["Institute"].unique())
)

# Filter by institute first
institute_df = df[df["Institute"] == institute]

# ================= YEAR =================
year = st.selectbox(
    "Select Year",
    sorted(institute_df["Year"].unique(), reverse=True)
)

year_df = institute_df[institute_df["Year"] == year]

# ================= ROUND =================
round_no = st.selectbox(
    "Select Round",
    sorted(year_df["Round"].unique())
)

round_df = year_df[year_df["Round"] == round_no]

# ================= PROGRAM =================
program = st.selectbox(
    "Select Program",
    sorted(round_df["Academic Program Name"].unique())
)

program_df = round_df[round_df["Academic Program Name"] == program]

# ================= CATEGORY =================
seat_type = st.selectbox(
    "Select Category",
    sorted(program_df["Seat Type"].unique())
)

seat_df = program_df[program_df["Seat Type"] == seat_type]

# ================= GENDER =================
gender = st.selectbox(
    "Select Gender",
    sorted(seat_df["Gender"].unique())
)

final = seat_df[seat_df["Gender"] == gender]

# ================= OUTPUT =================
if not final.empty:
    st.success("Cutoff Found")

    st.metric("Opening Rank", int(final.iloc[0]["Opening Rank"]))
    st.metric("Closing Rank", int(final.iloc[0]["Closing Rank"]))

    st.subheader("📈 Closing Rank Trend Over Years")

    trend = df[
        (df["Institute"] == institute) &
        (df["Academic Program Name"] == program) &
        (df["Seat Type"] == seat_type) &
        (df["Gender"] == gender)
    ]

    trend_data = trend.groupby("Year")["Closing Rank"].mean().reset_index()

    st.line_chart(trend_data.set_index("Year"))

else:
    st.warning("No cutoff data found.")