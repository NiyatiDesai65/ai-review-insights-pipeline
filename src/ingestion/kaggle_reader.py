import os
import pandas as pd
from src.logger import  get_logger
import kaggle
from config import (
    KAGGLE_DATASET,
    KAGGLE_FILE,
    RAW_DATA_PATH,
    MAX_REVIEWS
)


logger = get_logger("ingestion")

def download_dataset():
    logger.info(f"Downloading Dataset : {KAGGLE_DATASET}")
    
    try:
        #create folder if not exist
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            KAGGLE_DATASET,
            path=os.path.dirname(RAW_DATA_PATH),
            unzip=True
        )
        
        logger.info("Dataset downloaded successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to download Dataset : {e}")
        raise
    
def read_reviews():
    logger.info(f"Reading Reviews from {RAW_DATA_PATH}")
    
    try:
        # read only what we need
        df = pd.read_csv(RAW_DATA_PATH, nrows=MAX_REVIEWS)
        
        # keep only useful columns
        df = df[['Id', 'ProductId', 'Score', 'Summary', 'Text']]
        
        # rename columns to match our pipeline
        df = df.rename(columns={
            'Id': 'id',
            'ProductId': 'product_id',
            'Score': 'rating',
            'Summary': 'summary',
            'Text': 'review'
        })
        
        # drop rows with missing reviews
        df = df.dropna(subset=['review'])
        
        reviews = df.to_dict('records')
        logger.info(f"Read {len(reviews)} reviews successfully")
        return reviews
        
    except Exception as e:
        logger.error(f"Failed to read reviews: {e}")
        raise
    
def ingest():
    logger.info("Starting ingestion")
    download_dataset()
    reviews = read_reviews()
    logger.info(f"Ingestion complete. {len(reviews)} reviews ready.")
    return reviews
    
    