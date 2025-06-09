from scripts.rainfall_analysis import load_rainfall_data, summarize_rainfall, visualize_rainfall


def main():
    filepath = "data/precipitation_seoul_2024.csv"
    output_path = "output/seoul_rainfall_2024.png"

    df = load_rainfall_data(filepath)
    summarize_rainfall(df)
    visualize_rainfall(df, output_path)

if __name__ == "__main__":
    main()
