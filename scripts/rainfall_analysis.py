import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os

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

def visualize_rainfall(df: pd.DataFrame, output_path: str):
    station_map = {
        108: '서울',
        159: '부산',
        143: '대구',
        131: '인천',
        146: '광주',
        133: '대전',
        184: '제주'
    }
    matplotlib.rc('font', family='AppleGothic')
    matplotlib.rcParams['axes.unicode_minus'] = False

    station_code = int(df['지점'].iloc[0])
    region_name = station_map.get(station_code, f"알 수 없는 지역 (코드: {station_code})")

    # output 폴더 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(df['날짜'], df['강수량(mm)'], label='일별 강수량', color='blue')
    plt.title(f'2024년 {region_name} 일별 강수량')
    plt.xlabel('날짜')
    plt.ylabel('강수량 (mm)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # 저장
    plt.savefig(output_path)
    print(f"강수량 그래프 저장됨: {os.path.abspath(output_path)}")