import streamlit as st
import pandas as pd
from clean_weather import clean_weather, check_weather
from baseline import run_baseline
from optimizer import run_optimizer
from compare import make_comparison_chart
from checks import check_jobs,check_vessels

st.set_page_config(page_title="Vessel Scheduler", layout="wide")

st.title("🚢 Vessel Schedule Optimizer")
st.write("Efficiently scheduling the Jobs with available vessels")

#vessels = pd.read_csv("data/vessels_anon.csv")
#jobs = pd.read_csv("data/jobs_anon.csv")

with open("data/weather_cleaned.csv") as f:
    template = f.read()

st.sidebar.download_button(
    label="Download weather template",
    data=template,
    file_name="weather_template.csv",
    mime="text/csv",
)
with open("data/jobs_anon.csv") as f:
    template = f.read()

st.sidebar.download_button(
    label="Download jobs template",
    data=template,
    file_name="job_template.csv",
    mime="text/csv",
)
with open("data/vessels_anon.csv") as f:
    template = f.read()

st.sidebar.download_button(
    label="Download vessels template",
    data=template,
    file_name="vessels_template.csv",
    mime="text/csv",
)
st.sidebar.header("⚙️ Controls")
st.sidebar.write("Click to compare the baseline and optimized schedules")
uploaded = st.sidebar.file_uploader("Upload weather CSV", type="csv")
job_file = st.sidebar.file_uploader("Upload job CSV",type="csv")
vessel_file = st.sidebar.file_uploader("Upload vessels CSV", type="csv")
if uploaded is None:
    weather = pd.read_csv("data/weather_cleaned.csv")
else:
    raw = pd.read_csv(uploaded, dtype=str)
    problems = check_weather(raw)
    if len(problems) > 0:
        for error in problems:
            st.error(error)
        st.stop()
    weather = clean_weather(raw)
    st.sidebar.success("✅ Weather file loaded")

if job_file is None:
    jobs = pd.read_csv("data/jobs_anon.csv")
else:
    jobs = pd.read_csv(job_file, dtype=str)
    jobs = jobs.drop_duplicates()
    problems = check_jobs(jobs)
    if len(problems) > 0:
        for error in problems:
            st.error(error)
        st.stop()
    jobs["duration_days"] = jobs["duration_days"].astype(int)
    st.sidebar.success("✅ Jobs file loaded")


if vessel_file is None:
    vessels = pd.read_csv("data/vessels_anon.csv")
else:
    try:
        vessels = pd.read_csv(vessel_file, dtype=str)
    except pd.errors.EmptyDataError:
        st.error("The vessels file is empty.")
        st.stop()
    vessels = vessels.drop_duplicates()
    problems = check_vessels(vessels)
    if len(problems) > 0:
        for error in problems:
            st.error(error)
        st.stop()
    vessels["max_wave_height_m"] = vessels["max_wave_height_m"].astype(float)
    st.sidebar.success("✅Vessel file loaded")



run = st.sidebar.button("🚀 Run Scheduler", type="primary", width="stretch")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🚢 Vessels", len(vessels))
col2.metric("🛠️ Jobs", len(jobs))
col3.metric("📅 Weather days", len(weather))
col4.metric("🌊 Max wave limit (m)", vessels["max_wave_height_m"].max())

if run:
    with st.spinner("Optimizing schedule..."):
        base_schedule_table, last_finish = run_baseline(weather, vessels, jobs)
        optimized_schedule_table, last_day = run_optimizer(weather, vessels, jobs)
    st.success("Scheduling complete!")

    r1, r2, r3 = st.columns(3)
    r1.metric("Baseline finishes", f"Day {last_finish}")
    r2.metric("Optimizer finishes", f"Day {last_day}")
    r3.metric("Days saved", f"{last_finish - last_day} days")

    st.pyplot(make_comparison_chart(base_schedule_table, optimized_schedule_table))
    col_a, col_b = st.columns(2)
    col_a.subheader("Baseline schedule")
    col_a.dataframe(base_schedule_table, width="stretch", hide_index=True)
    col_a.download_button(label ="Download Baseline Schedule",
                          data = base_schedule_table.to_csv(index=False),
                          file_name="baseline_schedule.csv",
                          mime="text/csv",          
                          on_click="ignore"
                          )
    col_b.subheader("Optimized schedule")
    col_b.dataframe(optimized_schedule_table, width="stretch", hide_index=True)
    col_b.download_button(label ="Download Optimized Schedule",
                              data = optimized_schedule_table.to_csv(index=False),
                              file_name="optimized_schedule.csv",
                              mime="text/csv",
                              on_click="ignore"
                              )
else:
    st.info("👈 Upload your own weather , vessel or job CSV (optional), then click **Run Scheduler**.")

job_colors = {
    "Turbine installation": "#FDE68A",
    "Cable inspection": "#BFDBFE",
    "Buoy maintenance": "#BBF7D0",
    "Seabed survey": "#FBCFE8",
    "Mooring check": "#DDD6FE",
}

tab1, tab2, tab3 = st.tabs(["🚢 Vessels", "🛠️ Jobs", "🌦️ Weather"])

with tab1:
    st.dataframe(vessels, width="stretch", hide_index=True)

with tab2:
    if "job_type" in jobs.columns:
        st.dataframe(
            jobs.style.map(lambda v: f"background-color: {job_colors.get(v, '')}",
                           subset=["job_type"]),
            width="stretch", hide_index=True,
        )
    else:
        st.dataframe(jobs, width="stretch", hide_index=True)

with tab3:
    st.line_chart(weather, x="date", y="wave_height_m", color="#0EA5E9")
    st.dataframe(weather, width="stretch", hide_index=True)