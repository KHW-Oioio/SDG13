# data_loader.py
import os
import requests
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------- 예시용 더미 CSV 자동 생성 ------------ #
def _create_dummy_weather():
    csv_str = """date,RegionA,RegionB,RegionC
2022-01-01,5.2,3.1,4.8
2022-01-02,0.0,2.5,1.0
2022-01-03,1.2,0.0,0.5
2022-01-04,10.5,8.3,9.1
2022-01-05,3.3,6.2,2.8
"""
    with open(f"{DATA_DIR}/weather.csv", "w", encoding="utf-8") as f:
        f.write(csv_str)

def _create_dummy_disaster():
    csv_str = """year,region,damage_amount_hundred_million_won,deaths
2020,RegionA,1.5,2
2021,RegionB,0.8,0
2022,RegionC,2.1,1
2022,RegionA,1.2,0
"""
    with open(f"{DATA_DIR}/disaster.csv", "w", encoding="utf-8") as f:
        f.write(csv_str)

# --------------------------------------------------- #

def load_weather_data():
    path = f"{DATA_DIR}/weather.csv"
    if not os.path.exists(path):
        _create_dummy_weather()     # 실제 프로젝트에서는 API 호출
    df = pd.read_csv(path, parse_dates=["date"])
    # 🔑 인덱스로 바꾸지 않고 'date' 칼럼을 그대로 둔다
    return df

def load_disaster_data():
    path = f"{DATA_DIR}/disaster.csv"
    if not os.path.exists(path):
        _create_dummy_disaster()
    return pd.read_csv(path)
