import csv
import os
from datetime import datetime
from src.logger import get_logger
from config import RESULTS_PATH

logger = get_logger("reporting")

def save_results(results):
    logger.info(f"Saving {len(results)} results to {RESULTS_PATH}")
    
    try:
        os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
        fieldnames = [
            'id', 'product_id', 'rating', 'review',
            'sentiment', 'category', 'key_issue', 'confidence'
        ]
        
        with open(RESULTS_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        logger.info(f"Results saved successfully to {RESULTS_PATH}")
        
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        raise

def generate_report(results):
    logger.info("Generating report")
    
    total = len(results)
    
    if total == 0:
        logger.warning("No results to report")
        return
    
    # count sentiments
    sentiments = {}
    for r in results:
        s = r['sentiment']
        sentiments[s] = sentiments.get(s, 0) + 1
    
    # count categories
    categories = {}
    for r in results:
        c = r['category']
        categories[c] = categories.get(c, 0) + 1

    # count confidence
    confidence = {}
    for r in results:
        c = r['confidence']
        confidence[c] = confidence.get(c, 0) + 1
    
    # average rating
    avg_rating = sum(float(r['rating']) for r in results) / total

    report = []
    report.append("=" * 60)
    report.append(f"AMAZON REVIEW PIPELINE REPORT")
    report.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    report.append(f"\nTotal reviews processed: {total}")
    report.append(f"Average star rating: {avg_rating:.1f} / 5.0")
    
    report.append("\nSentiment breakdown:")
    for sentiment, count in sentiments.items():
        percentage = round((count / total) * 100)
        report.append(f"  {sentiment}: {count} ({percentage}%)")
    
    report.append("\nCategory breakdown:")
    for category, count in categories.items():
        percentage = round((count / total) * 100)
        report.append(f"  {category}: {count} ({percentage}%)")

    report.append("\nConfidence breakdown:")
    for level, count in confidence.items():
        percentage = round((count / total) * 100)
        report.append(f"  {level}: {count} ({percentage}%)")
    
    report.append("\nTop negative reviews to action:")
    negative = [r for r in results if r['sentiment'] == 'negative']
     # show top 5 only
    for r in negative[:5]: 
        report.append(f"  - Product {r['product_id']} (rated {r['rating']}/5): {r['key_issue']}")
    
    report.append("=" * 60)
    
    # print and log each line
    for line in report:
        logger.info(line)

def run(results):
    """Full reporting — save and generate report"""
    save_results(results)
    generate_report(results)