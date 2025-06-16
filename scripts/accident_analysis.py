import pandas as pd
import matplotlib.pyplot as plt
import os

def load_accident_data(filepath="data/accident.xls", output_path="output/seoul_accident_by_gu_2024.png"):
    # 엑셀 읽기
    xls = pd.ExcelFile(filepath)
    print("📄 시트 목록:", xls.sheet_names)

    # 시트 불러오기
    df = pd.read_excel(xls, sheet_name=0)
    df.columns = df.columns.str.strip()

    print("🧾 컬럼명:", df.columns.tolist())
    print("✅ 데이터 미리보기:")
    print(df.head())

    # 사고건수 데이터만 필터링
    filtered = df[(df['시도'] == '서울') & (df['사고년도'] == '사고[건]')]

    # 날짜 열만 선택
    date_columns = [col for col in filtered.columns if str(col).startswith('2024')]

    # 날짜 열 숫자로 변환 후 합산
    filtered[date_columns] = filtered[date_columns].apply(pd.to_numeric, errors='coerce')
    filtered['사고합계'] = filtered[date_columns].sum(axis=1)

    # 시군구별로 합계 집계
    summary = filtered.groupby('시군구')['사고합계'].sum().sort_values(ascending=False)

    # 시각화
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(12, 6))
    summary.plot(kind='bar', color='steelblue')
    plt.title('2024년 서울 시군구별 교통사고 건수')
    plt.xlabel('시군구')
    plt.ylabel('사고건수')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)

    print(f"✅ 사고 그래프 저장됨: {os.path.abspath(output_path)}")
