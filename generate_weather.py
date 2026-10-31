import random
import pandas as pd

random.seed(42)
heights = []
dates = pd.date_range("2026-11-01", periods=30, freq="D") 
for i in range(1,31):
    h = round(random.uniform(0.8, 3.5), 1)  
    heights.append(h)

table = pd.DataFrame({"date": dates, "wave_height_m": heights})
table.to_csv("data/weather_clean.csv", index=False)    
print(table.head(10))

