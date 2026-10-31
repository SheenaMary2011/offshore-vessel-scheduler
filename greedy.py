jobs = {"A":1,"B":3,"C":2}
storm_days= [3,7]


def isJobFeasible(startingDay,numberOfDays):
    for i in range(startingDay,startingDay+numberOfDays):
        if i in storm_days:
            return False

    return True




def greedy():
    starting_point = 1
    for job_name,job_days in jobs.items():
        start = starting_point
        jobAssigned = isJobFeasible(start,job_days)
        while not (jobAssigned):
            start = start+1
            jobAssigned = isJobFeasible(start,job_days)
        finish = start + job_days -1
        starting_point = finish+1
        print(f"Job {job_name} finish in {finish}")



greedy()
