import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_seoul_congestion_by_district(
    filepath: str = "data/traffic_jam.csv",
    output_path: str = "output/seoul_congestion_by_district.png"
):
    seoul_districts = [
        "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구",
        "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
        "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
        "서초구", "강남구", "송파구", "강동구"
    ]

    df = pd.read_csv(filepath, encoding="cp949")

    df = df[df["signgu_nm"].isin(seoul_districts)]

    summary = df.groupby("signgu_nm")["ave_road_cfi"].mean()
    filtered = summary[summary > 0].sort_values(ascending=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 시각화
    plt.figure(figsize=(14, 6))
    filtered.plot(kind='bar', color='skyblue')
    plt.title("서울시 자치구별 평균 도로혼잡도 (0 제외, 오름차순)", fontsize=14)
    plt.xlabel("자치구", fontsize=12)
    plt.ylabel("평균 도로혼잡도", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"서울 도로 혼잡도 그래프 저장됨: {os.path.abspath(output_path)}")
