import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_weather_data():
    df = pd.read_csv(f"{DATA_DIR}/weather.csv", parse_dates=["date"])
    return df

def load_disaster_data():
    df = pd.read_csv(f"{DATA_DIR}/disaster.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df
