# data_loader.py
import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def _create_dummy_disaster():
    csv_str = """year,region,damage_amount_hundred_million_won,deaths
2020,RegionA,1.5,2
2021,RegionB,0.8,0
2022,RegionC,2.1,1
2022,RegionA,1.2,0
"""
    with open(f"{DATA_DIR}/disaster.csv", "w", encoding="utf-8") as f:
        f.write(csv_str)

def load_disaster_data():
    path = f"{DATA_DIR}/disaster.csv"
    if not os.path.exists(path):
        _create_dummy_disaster()

    df = pd.read_csv(path)

    # 🔑 1) 칼럼 이름을 소문자·공백제거로 표준화
    df.columns = df.columns.str.strip().str.lower()

    # 🔑 2) 필수 칼럼 존재 확인
    required = {"region", "damage_amount_hundred_million_won"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(
            f"CSV에 {missing} 칼럼이 없습니다. "
            "칼럼 이름을 확인하거나 data_loader.py에서 매핑을 수정하세요."
        )
    return df
