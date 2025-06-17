import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def load_weather_data(api_key=None, city="Seoul", days=5, filepath='data/weather.csv'):
    if api_key is None:
        api_key = os.getenv('OWM_API_KEY', '')

    def fetch_weather_openweathermap():
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
            if resp.status_code != 200:
                print(f"API 요청 실패: 상태 코드 {resp.status_code}")
                continue
            data = resp.json()
            temps = [h['temp'] for h in data.get('hourly', []) if 'temp' in h]
            avg_temp = sum(temps) / len(temps) if temps else None
            records.append({
                'date': dt.strftime("%Y-%m-%d"),
                'avg_temp': avg_temp
            })

        if records:
            df = pd.DataFrame(records)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df.to_csv(filepath, index=False)
            print(f"날씨 데이터를 '{filepath}'에 저장했습니다.")
            return df
        else:
            print("날씨 데이터를 가져오지 못했습니다.")
            return pd.DataFrame(columns=['date', 'avg_temp'])

    # 파일 없거나 크기가 0이면 새로 받기
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        print(f"'{filepath}' 파일이 없거나 비어있어 API에서 데이터를 받아옵니다.")
        return fetch_weather_openweathermap()

    # 파일 존재하면 읽되, EmptyDataError 방어
    try:
        df = pd.read_csv(filepath, parse_dates=['date'])
        if df.empty:
            print(f"'{filepath}' 파일이 비어있습니다. API에서 데이터를 받아옵니다.")
            return fetch_weather_openweathermap()
        return df
    except pd.errors.EmptyDataError:
        print(f"'{filepath}' 파일 읽기 실패(EmptyDataError). API에서 데이터를 받아옵니다.")
        return fetch_weather_openweathermap()

