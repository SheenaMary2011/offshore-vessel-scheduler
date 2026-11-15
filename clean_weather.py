import pandas as pd
def check_weather(raw):
    problems = []
    file_headers = raw.columns 
    if 'date' not in file_headers:
        problems.append("Missing column: date")
    if 'wave_height_m' not in file_headers:
        problems.append("Missing column: wave_height_m")
    if len(problems)> 0:
        return problems
    if len(raw)==0:
        problems.append("The file has no rows of data")
    for value in raw["wave_height_m"]:
        try:
            fix_height(value)
        except ValueError:
            problems.append(f"'{value}' is not a valid wave height")
    for value in raw["date"]:
        if(pd.isna(value)):
            continue
        try:
            pd.to_datetime(fix_date(value))
        except ValueError:
            problems.append(f"'{value}' is not a date")

    return problems

def fix_date(text):
    # "12/11/2026" -> "2026-11-12"; anything else stays the same

    if "/" in text:
        day, month, year = text.split("/")
        return f"{year}-{month}-{day}"
    return text



def  fix_height(value):
    metres=0.0
    if pd.isna(value):
        return None
    if value.endswith("ft"):
        number_text = value[:-2]
        feet = float(number_text)
        metres = feet/3.28
    else:
        metres=float(value)
    if metres < 0 or metres >15:
        return None
    return round(metres,1)

def clean_weather(raw):
    raw = raw.dropna(subset=["date"])
    raw["date"] = raw["date"].apply(fix_date)
    raw["wave_height_m"] =  raw["wave_height_m"].apply(fix_height)
    raw= raw.drop_duplicates()
    return raw

if __name__ == "__main__":
    
    raw = pd.read_csv("data/weather_raw.csv", dtype=str)
    raw =clean_weather(raw)
    raw.to_csv("data/weather_cleaned.csv", index=False)
    print(raw)
    print("Rows:", len(raw))
