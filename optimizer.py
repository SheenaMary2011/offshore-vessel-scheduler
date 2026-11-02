import pandas as pd
from ortools.sat.python import cp_model
from baseline import get_storm_days, fits, HORIZON


def get_allowed_starts(duration, storm_days):
    allowed=[]
    for i in range(1,HORIZON+1):
        if fits(i,duration,storm_days):
            allowed.append(i)
    return allowed

def run_optimizer(weather, vessels, jobs):
    model = cp_model.CpModel()
    choices = {} 
    storm_days_by_vessel  = {}
        
    schedule =[]

    for index, vessel in vessels.iterrows():
        name = vessel["vessel_name"]
        limit = vessel["max_wave_height_m"]
        storms = get_storm_days(weather, limit)
        storm_days_by_vessel[name] = storms
    intervals_by_vessel = {}  
    for name in storm_days_by_vessel:
        intervals_by_vessel[name] = []  
    finish_days = []
    for index,job in jobs.iterrows():
        job_id = job["job_id"]
        duration = int(job["duration_days"])
        assigned_flags = []
                
        for name, storms in storm_days_by_vessel.items():
            allowed = get_allowed_starts(duration, storms)
            is_assigned = model.new_bool_var(f"{job_id}_on_{name}")
            start = model.new_int_var_from_domain(cp_model.Domain.from_values(allowed), f"{job_id}_start_{name}")
            finish = model.new_int_var(0, HORIZON, f"{job_id}_finish_{name}")
            model.add(finish == start + duration - 1).only_enforce_if(is_assigned)
            model.add(finish == 0).only_enforce_if(is_assigned.Not())
            finish_days.append(finish)
            interval = model.new_optional_interval_var(start, duration, start + duration, is_assigned, f"{job_id}_{name}")
            intervals_by_vessel[name].append(interval)
            assigned_flags.append(is_assigned)
            choices[(job_id, name)] = (is_assigned, start)
        model.add_exactly_one(assigned_flags) 
    for name, intervals in intervals_by_vessel.items():
        model.add_no_overlap(intervals)    

    last_day = model.new_int_var(0, HORIZON, "last_day")
    model.add_max_equality(last_day, finish_days)    # last_day = the latest finish of all jobs
    model.minimize(last_day) 
                            # make it as small as possible
    solver = cp_model.CpSolver()
    solver.solve(model)

     



    for (job_id, name), (is_assigned, start) in choices.items():
        if solver.value(is_assigned):
            start_day = solver.value(start)
            duration = int(jobs.loc[jobs["job_id"] == job_id, "duration_days"].iloc[0])
            schedule.append({"job_id": job_id, "vessel": name,
                                "start_day": start_day, "finish_day": start_day + duration - 1})

    schedule_table = pd.DataFrame(schedule).sort_values("start_day")

    return schedule_table, solver.value(last_day)
    

if __name__ == "__main__":
    
    weather = pd.read_csv("data/weather_cleaned.csv")
    vessels = pd.read_csv("data/vessels_anon.csv")
    jobs =   pd.read_csv("data/jobs_anon.csv")
    
    schedule_table,last_day = run_optimizer(weather,vessels,jobs)
    print(schedule_table)
    schedule_table.to_csv("data/optimized_schedule.csv", index=False)
    print("Optimized finishes on day", last_day)   





