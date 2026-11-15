import streamlit as st
import pandas as pd
from clean_weather import clean_weather
from clean_weather import check_weather
from baseline import run_baseline
from optimizer import run_optimizer
from compare import make_comparison_chart


st.set_page_config(page_title="Vessel Scheduler", layout="wide")

st.title("Offshore Vessel Scheduler")
st.write("Efficiently scheduling the Jobs with available vessels")

vessels = pd.read_csv("data/vessels_anon.csv")
jobs =   pd.read_csv("data/jobs_anon.csv")

st.sidebar.header("Controls")
st.sidebar.write("Click to compare the baseline and optimized schedules")
uploaded = st.sidebar.file_uploader("Upload weather CSV", type="csv")
if uploaded is None:
    weather = pd.read_csv("data/weather_cleaned.csv")
else:
    raw = pd.read_csv(uploaded, dtype=str)
    problems = check_weather(raw)
    if len(problems) >0:
        for error in problems:
            st.error(error)
        st.stop()
    weather = clean_weather(raw)
if st.sidebar.button("Run Scheduler"):
    base_schedule_table, last_finish=run_baseline(weather, vessels, jobs)
    optimized_schedule_table,last_day = run_optimizer(weather, vessels, jobs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline finishes", f"Day {last_finish}")
    col2.metric("Optimizer finishes", f"Day {last_day}")
    col3.metric("Days saved", f"{last_finish - last_day} days")
    fig =make_comparison_chart(base_schedule_table,optimized_schedule_table)
    st.pyplot(fig)
    col_a, col_b = st.columns(2)
    col_a.subheader("Baseline schedule")
    col_a.dataframe(base_schedule_table)
    col_b.subheader("Optimized schedule")
    col_b.dataframe(optimized_schedule_table)
    
st.subheader("Available Vessels")
st.dataframe(vessels)

st.subheader("Job List")
st.dataframe(jobs)

st.subheader("Weather Data")
st.dataframe(weather)
st.line_chart(weather, x="date", y="wave_height_m")



