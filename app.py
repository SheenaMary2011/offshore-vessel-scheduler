import streamlit as st
import pandas as pd

st.title("Offshore Vessel Scheduler")
st.write("Efficiently scheduling the Jobs with available vessels")

vessels = pd.read_csv("data/vessels_anon.csv")
jobs =   pd.read_csv("data/jobs_anon.csv")
weather = pd.read_csv("data/weather_cleaned.csv")

st.subheader("Available Vessels")
st.dataframe(vessels)

st.subheader("Job List")
st.dataframe(jobs)

st.subheader("Weather Data")
st.dataframe(weather)
st.line_chart(weather, x="date", y="wave_height_m")