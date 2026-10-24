import pandas as pd
import plotly.express as px
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Customer Feedback Analysis", page_icon="📊", layout="wide")
st.title("📊 Customer Feedback Analysis Using Python")
st.caption("Explore customer comments, sentiment, ratings, and recurring issues.")

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv("data/customer_feedback.csv")

uploaded = st.sidebar.file_uploader("Upload your feedback CSV (optional)", type=["csv"])
try:
    df = load_data(uploaded)
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

required = {"feedback", "rating"}
missing = required - set(df.columns)
if missing:
    st.error("CSV must include these columns: " + ", ".join(sorted(required)))
    st.stop()

df["feedback"] = df["feedback"].fillna("").astype(str)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["rating"])
df = df[df["feedback"].str.strip() != ""].copy()
if df.empty:
    st.warning("No usable feedback rows were found.")
    st.stop()

analyzer = SentimentIntensityAnalyzer()
df["sentiment_score"] = df["feedback"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
df["sentiment"] = df["sentiment_score"].apply(
    lambda x: "Positive" if x >= 0.05 else ("Negative" if x <= -0.05 else "Neutral")
)

st.sidebar.header("Filters")
if "category" in df.columns:
    categories_filter = st.sidebar.multiselect("Category", sorted(df["category"].dropna().astype(str).unique()),
                                                default=sorted(df["category"].dropna().astype(str).unique()))
    df = df[df["category"].astype(str).isin(categories_filter)]
if "customer_type" in df.columns:
    customer_types = st.sidebar.multiselect("Customer type", sorted(df["customer_type"].dropna().astype(str).unique()),
                                             default=sorted(df["customer_type"].dropna().astype(str).unique()))
    df = df[df["customer_type"].astype(str).isin(customer_types)]
min_rating, max_rating = st.sidebar.slider("Rating range", 1, 5, (1, 5))
df = df[df["rating"].between(min_rating, max_rating)]

if df.empty:
    st.info("No records match the selected filters.")
    st.stop()

total = len(df)
avg_rating = df["rating"].mean()
positive_pct = (df["sentiment"] == "Positive").mean() * 100
negative_pct = (df["sentiment"] == "Negative").mean() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Feedback records", f"{total:,}")
c2.metric("Average rating", f"{avg_rating:.2f} / 5")
c3.metric("Positive sentiment", f"{positive_pct:.1f}%")
c4.metric("Negative sentiment", f"{negative_pct:.1f}%")

left, right = st.columns(2)
with left:
    st.subheader("Sentiment distribution")
    sentiment_counts = df["sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Count")
    st.plotly_chart(px.pie(sentiment_counts, names="Sentiment", values="Count", hole=0.45),
                    use_container_width=True)
with right:
    st.subheader("Ratings distribution")
    rating_counts = df["rating"].value_counts().sort_index().rename_axis("Rating").reset_index(name="Count")
    st.plotly_chart(px.bar(rating_counts, x="Rating", y="Count", text="Count"),
                    use_container_width=True)

if "category" in df.columns:
    st.subheader("Sentiment by category")
    cat = df.groupby(["category", "sentiment"]).size().reset_index(name="Count")
    st.plotly_chart(px.bar(cat, x="category", y="Count", color="sentiment", barmode="group"),
                    use_container_width=True)

st.subheader("Feedback explorer")
sentiment_filter = st.multiselect("Show sentiment", ["Positive", "Neutral", "Negative"],
                                  default=["Positive", "Neutral", "Negative"])
view = df[df["sentiment"].isin(sentiment_filter)].copy()
columns = [c for c in ["feedback_id", "date", "customer_type", "category", "rating",
                       "sentiment", "sentiment_score", "feedback"] if c in view.columns]
st.dataframe(view[columns], use_container_width=True, hide_index=True)

csv_bytes = view.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered feedback as CSV", data=csv_bytes,
                   file_name="filtered_customer_feedback.csv", mime="text/csv")

st.subheader("Quick observations")
if "category" in df.columns:
    negative_by_category = df[df["sentiment"] == "Negative"].groupby("category").size().sort_values(ascending=False)
    if not negative_by_category.empty:
        st.write(f"- Category with the most negative comments in this filtered view: **{negative_by_category.index[0]}** ({negative_by_category.iloc[0]} comments).")
    else:
        st.write("- No negative comments in the current filtered view.")
st.write(f"- Average customer rating in this filtered view is **{avg_rating:.2f}/5**.")
st.caption("Sentiment is estimated with VADER lexicon rules; sarcasm, context, and mixed-language feedback may be misclassified.")
