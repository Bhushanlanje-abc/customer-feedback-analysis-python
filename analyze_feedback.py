"""Command-line analysis for the sample customer feedback CSV."""
from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DATA_PATH = Path(__file__).parent / "data" / "customer_feedback.csv"

def main():
    df = pd.read_csv(DATA_PATH)
    analyzer = SentimentIntensityAnalyzer()
    df["feedback"] = df["feedback"].fillna("").astype(str)
    df["sentiment_score"] = df["feedback"].apply(lambda text: analyzer.polarity_scores(text)["compound"])
    df["sentiment"] = df["sentiment_score"].apply(
        lambda score: "Positive" if score >= 0.05 else ("Negative" if score <= -0.05 else "Neutral")
    )
    print("\\nCUSTOMER FEEDBACK SUMMARY")
    print("=" * 32)
    print(f"Records analysed: {len(df)}")
    print(f"Average rating: {df['rating'].mean():.2f}/5")
    print("\\nSentiment counts:")
    print(df["sentiment"].value_counts().to_string())
    if "category" in df.columns:
        print("\\nAverage rating by category:")
        print(df.groupby("category")["rating"].mean().sort_values(ascending=False).round(2).to_string())
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    out_file = output / "feedback_with_sentiment.csv"
    df.to_csv(out_file, index=False)
    print(f"\\nDetailed results saved to: {out_file}")

if __name__ == "__main__":
    main()
