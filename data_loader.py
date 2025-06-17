import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st  # Streamlit 사용 가정

# ——————————————
# 1. OpenWeatherMap 날씨 데이터 수집 함수
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

        # 오류 체크 (API 제한 등)
        if 'hourly' not in data:
            st.warning(f"{dt.strftime('%Y-%m-%d')} 날짜의 데이터가 없습니다.")
            continue

        temps = [h['temp'] for h in data.get('hourly', [])]
        avg_temp = sum(temps) / len(temps) if temps else None
        records.append({
            'date': dt.strftime("%Y-%m-%d"),
            'avg_temp': avg_temp
        })

    df = pd.DataFrame(records)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/weather.csv', index=False)
    return df

# ——————————————
# 2. 기상청 태풍 정보 API 예제 함수
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
    try:
        items = resp.json()['response']['body'].get('items', {}).get('item', [])
    except Exception as e:
        st.error(f"기상청 API 오류: {e}")
        items = []

    df = pd.DataFrame(items)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/disaster.csv', index=False)
    return df

# ——————————————
# 3. 데이터 로딩 함수 (빈 파일 예외 처리 포함)
# ——————————————
def load_weather_data():
    filepath = 'data/weather.csv'
    api_key = os.getenv('OWM_API_KEY', '')

    # 파일 없거나 빈 파일이면 새로 데이터 받아오기
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        st.info("날씨 데이터 파일이 없거나 비어있어 API에서 새로 데이터를 받아옵니다.")
        fetch_weather_openweathermap(api_key)

    # 데이터 읽기 시도
    try:
        df = pd.read_csv(filepath, parse_dates=['date'])
    except pd.errors.EmptyDataError:
        st.error("weather.csv 파일이 비어있어 데이터를 불러올 수 없습니다.")
        df = pd.DataFrame()

    return df

def load_disaster_data():
    filepath = 'data/disaster.csv'
    service_key = os.getenv('KMA_TY_SERVICE_KEY', '')

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        today = datetime.now().strftime("%Y%m%d")
        st.info("재해 데이터 파일이 없거나 비어있어 API에서 새로 데이터를 받아옵니다.")
        fetch_typhoon_kma(service_key, today, today)

    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        st.error("disaster.csv 파일이 비어있어 데이터를 불러올 수 없습니다.")
        df = pd.DataFrame()

    return df

# ——————————————
# 4. Streamlit 앱 예시 부분
# ——————————————
def main():
    st.title("기상 데이터 시각화")

    weather_df = load_weather_data()
    if weather_df.empty:
        st.warning("날씨 데이터가 없습니다. API 키를 확인하거나 데이터를 다시 생성해주세요.")
        return

    # 지역(컬럼) 리스트 가져오기 (예시는 'avg_temp' 외 다른 컬럼 없으면 그냥 ['avg_temp']로 처리)
    region_list = weather_df.columns.drop('date').tolist()
    if not region_list:
        region_list = ['avg_temp']

    region = st.sidebar.selectbox("지역(시/도)", region_list)

    # 선택된 지역 데이터 시각화 예시
    st.line_chart(weather_df.set_index('date')[region])

    disaster_df = load_disaster_data()
    if disaster_df.empty:
        st.warning("태풍 데이터가 없습니다.")
    else:
        st.write("태풍 데이터 샘플:")
        st.dataframe(disaster_df.head())

if __name__ == "__main__":
    main()
