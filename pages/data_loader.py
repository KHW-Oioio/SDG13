import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# ——————————————
# 1. OpenWeatherMap 날씨 데이터 수집 예제
# ——————————————
def fetch_weather_openweathermap(api_key, city="Seoul", days=5):
    """
    OpenWeatherMap에서 최근 days일간의 일일 평균 기온 데이터를 가져와 CSV로 저장합니다.
    """
    records = []
    now = datetime.utcnow()
    for i in range(days):
        dt = now - timedelta(days=i)
        timestamp = int(dt.replace(hour=12, minute=0, second=0).timestamp())
        url = (
            f"https://api.openweathermap.org/data/2.5/onecall/timemachine"
            f"?lat=37.5665&lon=126.9780&dt={timestamp}"
            f"&units=metric&appid={api_key}"
        )
        resp = requests.get(url)
        data = resp.json()
        temps = [h['temp'] for h in data.get('hourly', [])]
        records.append({
            'date': dt.strftime("%Y-%m-%d"),
            'avg_temp': sum(temps) / len(temps) if temps else None
        })

    df = pd.DataFrame(records)
    df.to_csv('data/weather.csv', index=False)
    return df

# ——————————————
# 2. 기상청 태풍 정보 API 예제
# ——————————————
def fetch_typhoon_kma(service_key, from_date, to_date):
    """
    기상청 태풍정보(Open API)에서 지정 기간 태풍 데이터를 가져와 CSV로 저장합니다.
    """
    url = "http://apis.data.go.kr/1360000/TyphoonInfoService/getTyphoonInfo"
    params = {
        'ServiceKey': service_key,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'JSON',
        'fromTmFc': from_date,  # YYYYMMDD
        'toTmFc': to_date       # YYYYMMDD
    }
    resp = requests.get(url, params=params)
    items = resp.json()['response']['body'].get('items', {}).get('item', [])
    df = pd.DataFrame(items)
    df.to_csv('data/disaster.csv', index=False)
    return df

# ——————————————
# 3. load functions for Streamlit app
# ——————————————
def load_weather_data():
    api_key = os.getenv('OWM_API_KEY', '')
    if not os.path.exists('data/weather.csv'):
        fetch_weather_openweathermap(api_key)
    return pd.read_csv('data/weather.csv', parse_dates=['date'])

def load_disaster_data():
    service_key = os.getenv('KMA_TY_SERVICE_KEY', '')
    if not os.path.exists('data/disaster.csv'):
        today = datetime.now().strftime("%Y%m%d")
        fetch_typhoon_kma(service_key, today, today)
    return pd.read_csv('data/disaster.csv')

