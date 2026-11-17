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
        problems.append(f" Job ID '{job}' appears more than once")
    for duration in jobs["duration_days"]:
        try:
            if int(duration) <=0:
                problems.append(f"'{duration}' must be a whole number of days, above 0")
        except  ValueError:
            problems.append(f"Job ID '{duration}' is not a valid value")

    return problems