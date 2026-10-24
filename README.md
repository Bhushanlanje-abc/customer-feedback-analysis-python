# Customer Feedback Analysis Using Python

A beginner-friendly Python project that analyzes customer comments and ratings using sentiment analysis. It includes an interactive Streamlit dashboard, a sample CSV dataset, charts, filtering, and CSV export.

## Features

- Positive, neutral, and negative sentiment classification using VADER.
- Average customer rating and sentiment percentage calculations.
- Sentiment distribution and rating charts.
- Sentiment analysis by category.
- Filters for category, customer type, rating, and sentiment.
- Upload your own customer feedback CSV file.
- Download filtered analysis results.
- Command-line analysis script that exports results to CSV.

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- VADER Sentiment Analysis

## Project Structure

```text
customer-feedback-analysis-python/
├── app.py
├── analyze_feedback.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── customer_feedback.csv
└── output/
    └── .gitkeep
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Open the project folder

```bash
cd customer-feedback-analysis-python
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows:**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Run the Analysis Script

Run the following command:

```bash
python analyze_feedback.py
```

The script displays a summary of the feedback and saves the detailed results to:

`output/feedback_with_sentiment.csv`

## Dataset

The included sample dataset contains 120 synthetic customer feedback records with fields such as:

- Feedback ID
- Date
- Customer type
- Category
- Rating
- Feedback text

You can also upload your own CSV file through the dashboard.

Your CSV must contain these columns:

- `feedback` — customer comment text
- `rating` — numeric customer rating

Optional columns include `category`, `customer_type`, `feedback_id`, and `date`.

## What I Learned

- Data loading and preprocessing using Pandas.
- Sentiment analysis using VADER.
- Data visualization using Plotly.
- Building interactive dashboards with Streamlit.
- Filtering and exporting datasets.
- Organizing a Python project and managing dependencies.

## Limitations

The included dataset is synthetic and intended for demonstration and learning. VADER is a lexicon-based sentiment analysis tool and may misclassify sarcasm, context-dependent statements, and multilingual feedback.

## Future Improvements

- Add machine learning-based sentiment classification.
- Perform keyword and topic analysis.
- Add more detailed customer satisfaction reports.
- Deploy the dashboard online.

---

Author: Bhushan Lanje
