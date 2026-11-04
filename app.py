import streamlit as st
import pandas as pd

st.title("OffShore Vessel Scheduler")
st.write("effeciently scheduling the Jobs with available vessels")

vessels = pd.read_csv("data/vessels_anon.csv")
jobs =   pd.read_csv("data/jobs_anon.csv")

vessels_table = pd.DataFrame(vessels)
jobs_table = pd.DataFrame(jobs)

st.subheader("Available Vessel")
st.dataframe(vessels_table)

st.subheader("Job List")
st.dataframe(jobs_table)