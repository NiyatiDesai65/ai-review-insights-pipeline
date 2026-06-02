# AI Review Insights Pipeline

A production-ready automated data pipeline that analyses real Amazon 
product reviews using Claude AI and Apache Airflow.

Built with real data from Kaggle — 500,000+ Amazon Fine Food Reviews dataset.

## What this does
- Downloads real Amazon reviews from Kaggle automatically
- Cleans and validates the data (removes nulls, duplicates, empty reviews)
- Sends each review to Claude AI for deep analysis
- Extracts sentiment, category, key issue and confidence score
- Saves results to CSV and generates a business report
- Runs automatically every day via Apache Airflow

## Pipeline architecture
Kaggle Dataset
↓
Ingestion (kaggle_reader.py)
↓
Cleaning (cleaner.py) — removes nulls, duplicates, empty reviews
↓
AI Analysis (analyzer.py) — Claude AI extracts insights
↓
Reporting (reporter.py) — saves CSV + generates report

## Project structure
ai-review-insights-pipeline/
├── dags/                    # Airflow DAG
├── src/
│   ├── ingestion/           # Kaggle data download
│   ├── processing/          # Data cleaning
│   ├── ai/                  # Claude AI analysis
│   └── reporting/           # Report generation
├── include/results/         # Pipeline output
├── logs/                    # Pipeline logs
├── tests/                   # Unit and integration tests
└── config.py                # All settings in one place

## Tech stack
- Python
- Apache Airflow (Astronomer Astro CLI)
- Anthropic Claude API
- Kaggle API
- Pandas
- Docker

## Sample output
See `include/results/results.csv` for real pipeline output.
See `logs/pipeline.log` for real pipeline logs.

## How to run
Install Astro CLI and Docker Desktop.

Add your keys to `.env`:
ANTHROPIC_API_KEY=your-key
KAGGLE_USERNAME=your-username
KAGGLE_KEY=your-key

Start Airflow:
astro dev start

Open http://localhost:8080 and trigger `amazon_review_pipeline`.
or run locally
python tests/test_pipeline.py

## Tests
python tests/test_cleaner.py
python tests/test_pipeline.py

## Dataset
Amazon Fine Food Reviews from Kaggle
500,000+ real product reviews
Source: https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews