import pandas as pd
client_codes = {}
jobs = pd.read_csv("data/jobs.csv") 

number =1;
for name in jobs["client_name"].unique():
    client_codes[name] = f"CLIENT_{number}"
    number = number+1
jobs["client_name"] = jobs["client_name"].map(client_codes)
jobs.to_csv("data/jobs_anon.csv", index=False)
print(jobs.head())  