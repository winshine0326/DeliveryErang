import pandas as pd

def load_rainfall_data(filepath: str) -> pd.DataFrame:
    """CSV 파일에서 강수량 데이터 불러오기"""
    df = pd.read_csv(filepath, encoding='cp949', skiprows=7)
    df.columns = ['날짜', '지점', '강수량(mm)']
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['강수량(mm)'] = pd.to_numeric(df['강수량(mm)'], errors='coerce')
    return df

def summarize_rainfall(df: pd.DataFrame):
    station_map = {
        108: '서울',
        159: '부산',
        143: '대구',
        131: '인천',
        146: '광주',
        133: '대전',
        184: '제주'
        # 필요 시 더 추가
    }

    station_code = int(df['지점'].iloc[0])
    """강수량 통계 요약 출력"""
    total_days = len(df) - 1
    zero_rain_days = (df['강수량(mm)'] == 0).sum()
    max_rain = df['강수량(mm)'].max()
    max_day = df[df['강수량(mm)'] == max_rain]['날짜'].values[0]
    region_name = station_map.get(station_code)

    print(f"분석 지역: {region_name} (지점 코드 {station_code})")
    print(f"총 일수: {total_days}일")
    print(f"비 안 온 날: {zero_rain_days}일 ({zero_rain_days / total_days:.1%})")
    print(f"최대 강수량: {max_rain}mm on {max_day}")
