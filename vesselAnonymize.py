import pandas as pd

vessels = pd.read_csv("data/vessels.csv") 
vessel_code={}
operator_code={}

number =1
for name in vessels["vessel_name"]:
    vessel_code[name] = f"VESSEL_{number}"
    number= number+1

count=1

for name in vessels["operator"]:
    operator_code[name] = f"OPERATOR_{count}"
    count=count+1

vessels["vessel_name"] = vessels["vessel_name"].map(vessel_code)
vessels["operator"] = vessels["operator"].map(operator_code)

vessels.to_csv("data/vessles_anon.csv", index=False)

