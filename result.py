# result.py

import pandas as pd
from scripts.accident_analysis import load_accident_data
from scripts.traffic_jam import visualize_seoul_congestion_by_district
from scripts.rainfall_analysis import load_rainfall_data, summarize_rainfall
import matplotlib.pyplot as plt
import os


def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def result():
    accident_filepath = "data/accident.xls"
    load_accident_data(filepath=accident_filepath)  # 시각화와 summary 출력

    df_accident = pd.read_excel(accident_filepath, sheet_name=0)
    df_accident.columns = df_accident.columns.str.strip()
    filtered = df_accident[(df_accident['시도'] == '서울') & (df_accident['사고년도'] == '사고[건]')]
    date_columns = [col for col in filtered.columns if str(col).startswith('2024')]
    filtered.loc[:, date_columns] = filtered[date_columns].apply(pd.to_numeric, errors='coerce')
    filtered.loc[:, '사고합계'] = filtered[date_columns].sum(axis=1)
    accident_df = filtered.groupby('시군구')['사고합계'].sum().reset_index()
    accident_df.columns = ['signgu_nm', '사고합계']

    traffic_path = "data/traffic_jam.csv"
    visualize_seoul_congestion_by_district(filepath=traffic_path)

    df_traffic = pd.read_csv(traffic_path, encoding='cp949')
    seoul_gu = [
        "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구",
        "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
        "서초구", "강남구", "송파구", "강동구"
    ]
    df_traffic = df_traffic[df_traffic["signgu_nm"].isin(seoul_gu)]
    congestion_df = df_traffic.groupby("signgu_nm")["ave_road_cfi"].mean().reset_index()

    merged = pd.merge(accident_df, congestion_df, on="signgu_nm")
    merged['accident_norm'] = normalize(merged['사고합계'])
    merged['congestion_norm'] = normalize(merged['ave_road_cfi'])
    merged['delivery_score'] = (
        (1 - merged['congestion_norm']) * 0.6 +
        (1 - merged['accident_norm']) * 0.4
    )
    result_df = merged.sort_values(by="delivery_score", ascending=False)
    print("서울시 배달하기 좋은 동네 순위 (상위 5):")
    print(result_df[['signgu_nm', '사고합계', 'ave_road_cfi', 'delivery_score']].head())

    rainfall_df = load_rainfall_data("data/precipitation_seoul_2024.csv")
    summarize_rainfall(rainfall_df)

    result_df.to_csv("output/seoul_delivery_score.csv", index=False)

    os.makedirs("output", exist_ok=True)

    # 시각화
    plt.figure(figsize=(14, 6))
    plt.bar(result_df["signgu_nm"], result_df["delivery_score"], color="mediumseagreen")
    plt.title("서울시 자치구별 배달하기 좋은 점수 순위 (높을수록 유리)", fontsize=14)
    plt.xlabel("자치구", fontsize=12)
    plt.ylabel("배달 점수", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y')
    plt.tight_layout()

    output_path = "output/seoul_delivery_score.png"
    plt.savefig(output_path)
    print(f"📊 배달 점수 그래프 저장됨: {os.path.abspath(output_path)}")