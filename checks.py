import pandas as pd

def check_vessels(vessels):
    problems = []
    file_headers = vessels.columns 
    if 'vessel_name' not in file_headers:
        problems.append("Missing column: vessel_name")
    if 'max_wave_height_m' not in file_headers:
        problems.append("Missing column: max_wave_height_m")
    if len(problems)> 0:
        return problems
    if len(vessels)==0:
        problems.append("The file has no rows of data")
    repeats = vessels["vessel_name"].duplicated()
    repeated_vessels = vessels["vessel_name"][repeats]

    for vessel in repeated_vessels.unique():
        problems.append(f"Vessel '{vessel}' appears more than once")
    for wave_height in vessels["max_wave_height_m"]:
        if pd.isna(wave_height):
                problems.append("A vessel is missing its wave limit")
                continue
        try:
            if float(wave_height) <=0:
                problems.append(f" wave limit'{wave_height}' must be a  number above 0")
            
        except  ValueError:
            problems.append(f" wave limit'{wave_height}' must be a  number above 0")

    return problems

def check_jobs(jobs):
    problems = []
    file_headers = jobs.columns 
    if 'job_id' not in file_headers:
        problems.append("Missing column: job_id")
    if 'duration_days' not in file_headers:
        problems.append("Missing column: duration_days")
    if len(problems)> 0:
        return problems
    if len(jobs)==0:
        problems.append("The file has no rows of data")
    repeats = jobs["job_id"].duplicated()
    repeated_jobIds = jobs["job_id"][repeats]

    for job in repeated_jobIds.unique():
        problems.append(f"Job ID '{job}' appears more than once")
    for duration in jobs["duration_days"]:
        try:
            if int(duration) <=0:
                problems.append(f"'{duration}' must be a whole number of days, above 0")
        except  ValueError:
            problems.append(f"Duratiomn '{duration}' is not a valid value")

    return problems