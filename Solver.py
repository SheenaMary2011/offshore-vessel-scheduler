from ortools.sat.python import cp_model
jobs = {"A":1,"B":3,"C":2}
storm_days= [2,5,7]
model = cp_model.CpModel()
starts = {}          # job name -> its start variable
intervals = []       # busy blocks, for the "no overlap" rule
finish_days = []     # each job's finish day, for the goal

def get_allowed_days(duration):
      allowed = []
      for i in range(1,16-duration+1):
            jobFeasible = isJobFeasible(i,duration)
            if(jobFeasible):
                allowed.append(i)
        
      return allowed

def isJobFeasible(startingDay,numberOfDays):
    for i in range(startingDay,startingDay+numberOfDays):
        if i in storm_days:
            return False

    return True

for job_name, job_days in jobs.items():
    print(job_name, get_allowed_days(job_days))


# --- PART 1: one start variable + one interval PER JOB ---
for job_name, job_days in jobs.items():
    allowed = get_allowed_days(job_days)

    start = model.new_int_var_from_domain(
        cp_model.Domain.from_values(allowed), f"start_{job_name}")

    interval = model.new_interval_var(
        start, job_days, start + job_days, f"job_{job_name}")
    print(interval)

    starts[job_name] = start
    intervals.append(interval)
    finish_days.append(start+job_days-1)

# --- PART 2: the rule (outside the loop) ---
model.add_no_overlap(intervals)          # one vessel: no two jobs at the same time

# --- PART 3: the goal ---
last_day = model.new_int_var(1, 15, "last_day")
model.add_max_equality(last_day, finish_days)   # last_day = latest finish of all jobs
model.minimize(last_day)                        # make that as small as possible

# --- PART 4: solve and print ---
solver = cp_model.CpSolver()
solver.solve(model)

for job_name in jobs:
    print(f"{job_name} starts day {solver.value(starts[job_name])}")
print("Last day:", solver.value(last_day))



