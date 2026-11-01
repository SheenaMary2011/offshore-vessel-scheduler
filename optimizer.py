import pandas as pd
from ortools.sat.python import cp_model
from baseline import get_storm_days, fits, HORIZON


def get_allowed_starts(duration, storm_days):
    allowed=[]
    for i in range(1,HORIZON+1):
        if fits(i,duration,storm_days):
            allowed.append(i)
    return allowed


if __name__ == "__main__":
    weather = pd.read_csv("data/weather_cleaned.csv")
    vessels = pd.read_csv("data/vessels_anon.csv")
    jobs =   pd.read_csv("data/jobs_anon.csv")
    storm_days_by_vessel  = {}
    
    schedule =[]

    for index, vessel in vessels.iterrows():
        name = vessel["vessel_name"]
        limit = vessel["max_wave_height_m"]
        storms = get_storm_days(weather, limit)
        storm_days_by_vessel[name] = storms
    for index,job in jobs.iterrows():
        job_id = job["job_id"]
        duration = job["duration_days"]
        for name, storms in storm_days_by_vessel.items():
            print(job_id, name, get_allowed_starts(duration, storms))


        





