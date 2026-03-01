import streamlit as st
import pandas as pd

st.title("📊 Placement Insights")

df = pd.read_csv("data/placedata v2.0 synthetic.csv")

st.dataframe(df.head())

st.bar_chart(df["salary"])