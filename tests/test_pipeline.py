import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.kaggle_reader import read_reviews
from src.processing.cleaner import clean
from src.ai.analyzer import analyse
from src.reporting.reporter import run
from src.logger import get_logger

logger = get_logger("test")

def test_full_pipeline():
    logger.info("Starting full pipeline test")
    
    # step 1 - read
    logger.info("Step 1 - Reading reviews")
    reviews = read_reviews()
    logger.info(f"Read {len(reviews)} reviews")
    
    # step 2 - clean
    logger.info("Step 2 - Cleaning reviews")
    cleaned = clean(reviews)
    logger.info(f"Cleaned {len(cleaned)} reviews")
    
    # step 3 - analyse (only first 5 to save API calls)
    logger.info("Step 3 - Analysing reviews")
    results = analyse(cleaned[:5])
    logger.info(f"Analysed {len(results)} reviews")
    
    # step 4 - report
    logger.info("Step 4 - Generating report")
    run(results)
    
    logger.info("Pipeline test complete")

if __name__ == "__main__":
    test_full_pipeline()