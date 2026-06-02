import time
import json
import anthropic
from src.logger import get_logger
from config import (
    ANTHROPIC_API_KEY,
    SLEEP_BETWEEN_CALLS,
    MAX_RETRIES,
    BATCH_SIZE
)

logger = get_logger('ai')

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def safe_parse_json(reply):
    reply = reply.strip()
    #print("Before parse:", repr(reply[:50])) 
    if reply.startswith("```"):
        reply = reply.split("```")[1]
        if reply.startswith("json"):
            reply = reply[4:]
        reply = reply.strip()
    #print("After clean:", repr(reply[:50]))  
    return json.loads(reply)

def analyse_single(review):
    """Analyse one review with Claude. Retry if it fails."""
    
    for attempt in range(MAX_RETRIES):
        try:
            response = anthropic_client.messages.create(
                model="claude-opus-4-5",
                max_tokens=200,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyse this product review and respond ONLY with JSON.
                                    No extra text. Just the JSON.

                                    Review: {review['review']}
                                    Star rating: {review['rating']} out of 5
                                    Respond with exactly this format
                                    {{
                                        "sentiment": "positive or negative or neutral",
                                        "category": "product quality or shipping or customer service or value for money",
                                        "key_issue": "one short phrase describing the main point",
                                        "confidence": "high or medium or low"
                                    }}"""
                    }
                ]
            )
            
            result = safe_parse_json(response.content[0].text)
            time.sleep(SLEEP_BETWEEN_CALLS)
            return result
            
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for review {review['id']}: {e}")
            
            if attempt < MAX_RETRIES - 1:
                wait_time = (attempt + 1) * 2  # wait 2s, 4s, 6s
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"All {MAX_RETRIES} attempts failed for review {review['id']}")
                return {
                    "sentiment": "unknown",
                    "category": "unknown",
                    "key_issue": "analysis failed",
                    "confidence": "low"
                }

def analyse_batch(reviews):
    logger.info(f"Analysing batch of {len(reviews)} reviews")
    results = []
    
    for i, review in enumerate(reviews):
        logger.info(f"Analysing review {i+1}/{len(reviews)} - id: {review['id']}")
        
        analysis = analyse_single(review)
        
        result = {
            'id': review['id'],
            'product_id': review['product_id'],
            'rating': review['rating'],
            'review': review['review'],
            'sentiment': analysis['sentiment'],
            'category': analysis['category'],
            'key_issue': analysis['key_issue'],
            'confidence': analysis['confidence']
        }
        results.append(result)
    
    logger.info(f"Batch analysis complete. {len(results)} reviews analysed.")
    return results

def analyse(reviews):
    logger.info(f"Starting AI analysis for {len(reviews)} reviews")
    all_results = []
    
    # split into batches
    for i in range(0, len(reviews), BATCH_SIZE):
        batch = reviews[i:i + BATCH_SIZE]
        logger.info(f"Processing batch {i//BATCH_SIZE + 1} - reviews {i+1} to {i+len(batch)}")
        
        batch_results = analyse_batch(batch)
        all_results.extend(batch_results)
    
    logger.info(f"AI analysis complete. Total: {len(all_results)} reviews analysed.")
    return all_results