
import os
from dotenv import load_dotenv

load_dotenv()

# ---- API keys ----
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

# ---- pipeline settings ----
BATCH_SIZE = 50           # process 50 reviews at a time
MAX_RETRIES = 3           # retry failed API calls 3 times
SLEEP_BETWEEN_CALLS = 0.5 # seconds between Claude API calls

# ---- dataset settings ----
KAGGLE_DATASET = "snap/amazon-fine-food-reviews"
KAGGLE_FILE = "Reviews.csv"
MAX_REVIEWS = 100         # how many reviews to process per run

# ---- file paths ----
RAW_DATA_PATH = "include/raw/reviews.csv"
RESULTS_PATH = "include/results/results.csv"
LOG_PATH = "logs/pipeline.log"