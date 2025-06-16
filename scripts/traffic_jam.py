import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_least_congested_districts(
    filepath: str = "data/traffic_jam.csv",
    output_path: str = "output/least_congestion_by_district.png",
    top_n: int = 10
):
    df = pd.read_csv(filepath, encoding="cp949")

    summary = df.groupby("signgu_nm")["ave_road_cfi"].mean()

    filtered = summary[summary > 0].sort_values()

    bottom_summary = filtered.head(top_n)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(12, 6))
    bottom_summary.plot(kind='bar', color='skyblue')
    plt.title(f"시군구별 평균 도로혼잡도 (하위 {top_n}개, 0 제외)", fontsize=14)
    plt.xlabel("시군구", fontsize=12)
    plt.ylabel("평균 도로혼잡도", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()

    # 저장
    plt.savefig(output_path)
    print(f"도로 혼잡도 그래프 저장됨: {os.path.abspath(output_path)}")
