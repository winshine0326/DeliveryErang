import pandas as pd
import matplotlib.pyplot as plt
import os


def load_accident_data(filepath="data/accident.xls", output_path="output/seoul_accident_2024.png"):
    # 엑셀 읽기
    xls = pd.ExcelFile(filepath)
    print("📄 시트 목록:", xls.sheet_names)

    # 첫 번째 시트 읽기
    df = pd.read_excel(xls, sheet_name=0)
    df.columns = df.columns.str.strip()  # 컬럼명 정리

    print("🔍 정리된 컬럼명:", df.columns.tolist())
    print("✅ 데이터 미리보기:")
    print(df.head())

    # 서울 + 사고[건] 필터
    filtered = df[(df['시도'] == '서울') & (df['사고년도'] == '사고[건]')]

    # 날짜 컬럼만 추출 (2024, 2024.1, ..., 2024.30)
    date_columns = [col for col in df.columns if str(col).startswith('2024')]

    # 월별 합계 계산
    filtered['사고월'] = filtered['사고월'].str.replace('월', '').astype(int)
    summary = filtered[date_columns].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    result = pd.DataFrame({
        '사고월': filtered['사고월'],
        '사고건수': summary
    }).groupby('사고월')['사고건수'].sum()

    # 시각화
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(10, 5))
    result.plot(kind='bar', color='tomato')
    plt.title('2024년 서울 월별 교통사고 건수')
    plt.xlabel('월')
    plt.ylabel('사고건수')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)

    print(f"✅ 사고 그래프 저장됨: {os.path.abspath(output_path)}")
