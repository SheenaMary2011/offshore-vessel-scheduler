import pandas as pd

HORIZON = 30

def get_storm_days(weather, max_wave):
    start_date = pd.to_datetime(weather["date"]).min() 
    storm_days=[]
    for index,row in weather.iterrows():
        date=pd.to_datetime(row["date"])
        day = (date - start_date).days + 1 
        wave_height = row["wave_height_m"]
        if(pd.isna(wave_height) or wave_height > max_wave):
            storm_days.append(day)
    return storm_days

def fits(start,duration,stormDays):
    lastday= start+duration -1
    if(lastday >HORIZON):
        return False
    for i in range(start,start+duration):
        if i in stormDays:
            return False
    return True
   
        
def run_baseline(weather, vessels, jobs):
    storm_days_by_vessel  = {}
    next_free_day={}
    schedule =[]
    
    for index, vessel in vessels.iterrows():
        name = vessel["vessel_name"]
        limit = vessel["max_wave_height_m"]
        storms = get_storm_days(weather, limit)
        storm_days_by_vessel[name] = storms
        next_free_day[name] = 1
            
        
        
    last_finish = 0
    
    for index, job in jobs.iterrows():
        job_id = job["job_id"]
        duration = job["duration_days"]

        best_vessel = None
        best_start = None

        for vessel,stormDays in storm_days_by_vessel.items():
            start = next_free_day[vessel]
            while not fits(start,duration,stormDays) and start < HORIZON:
                start = start+1
            if fits(start, duration, stormDays) and (best_start is None or start < best_start):
                best_start=start
                best_vessel = vessel
        if best_vessel is None:
            print(f"{job_id} could not be scheduled within {HORIZON} days")
            continue      # skip to the next job (same as Java's continue)
        finish  = best_start + duration-1
        next_free_day[best_vessel]= finish+1
        if finish > last_finish:
            last_finish=finish
        
        schedule.append({"job_id": job_id,
                "vessel": best_vessel,
                "start_day": best_start,
                "finish_day": finish,})
    
            
    schedule_table = pd.DataFrame(schedule)
    return schedule_table, last_finish      



if __name__ == "__main__":
    weather = pd.read_csv("data/weather_cleaned.csv")
    vessels = pd.read_csv("data/vessels_anon.csv")
    jobs = pd.read_csv("data/jobs_anon.csv")

    schedule_table, last_finish = run_baseline(weather, vessels, jobs)
    print(schedule_table)
    schedule_table.to_csv("data/baseline_schedule.csv", index=False)
    print(f"Baseline finishes on day {last_finish}")             


    