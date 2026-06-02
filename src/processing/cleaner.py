"""
    1.loops through every review
    2.calls clean_review(review) for each one
        [calls clean_text() on summary field
         calls clean_text() on review field ]
    3. then removes duplicates
    4. then removes empty ones
"""

import re
from src.logger import get_logger

logger = get_logger("processing")

#Cleans a single review text
def clean_text(text):
    if not text or not isinstance(text, str):
        return ""

    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    if len(text) > 500:
        text = text[:500] + "..."
    
    return text

def remove_nulls(reviews):
    clean = []
    
    for review in reviews:
        if (review.get('review') and 
            review.get('id') and 
            review.get('product_id')):
            clean.append(review)
    
    removed = len(reviews) - len(clean)
    if removed > 0:
        logger.info(f"Removed {removed} reviews with null values")
    
    return clean

def clean_review(review):
    return {
        'id': review.get('id', ''),
        'product_id': review.get('product_id', ''),
        'rating': review.get('rating', 0),
        'summary': clean_text(str(review.get('summary', ''))),
        'review': clean_text(str(review.get('review', '')))
    }

def remove_duplicates(reviews):
    seen = set()
    unique = []
    
    for review in reviews:
        # use review text as unique key
        key = review['review'][:100]
        if key not in seen:
            seen.add(key)
            unique.append(review)
    
    removed = len(reviews) - len(unique)
    if removed > 0:
        logger.info(f"Removed {removed} duplicate reviews")
    
    return unique

def remove_empty(reviews):
    clean = [r for r in reviews if r['review'].strip()]
    removed = len(reviews) - len(clean)
    
    if removed > 0:
        logger.info(f"Removed {removed} empty reviews")
    
    return clean

def clean(reviews):
    logger.info(f"Starting cleaning. Input: {len(reviews)} reviews")
    
    reviews = [clean_review(r) for r in reviews]
    reviews = remove_nulls(reviews)
    reviews = remove_duplicates(reviews)
    reviews = remove_empty(reviews)
    
    logger.info(f"Cleaning complete. Output: {len(reviews)} reviews")
    return reviews