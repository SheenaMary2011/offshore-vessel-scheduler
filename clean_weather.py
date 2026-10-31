import pandas as pd


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


if __name__ == "__main__":
    
    raw = pd.read_csv("data/weather_raw.csv", dtype=str)
    # 2. Run fix_date on every value in the date column
    raw["date"] = raw["date"].apply(fix_date)
    raw["wave_height_m"] =  raw["wave_height_m"].apply(fix_height)
    raw= raw.drop_duplicates()
    raw.to_csv("data/weather_cleaned.csv", index=False)

    print(raw)
    print("Rows:", len(raw))
