import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.processing.cleaner import (
    clean_text,
    remove_nulls,
    remove_duplicates,
    remove_empty,
    clean
)

# ---- test clean_text ----

def test_clean_text_removes_extra_spaces():
    result = clean_text("hello    world")
    assert result == "hello world", f"Expected 'hello world' but got '{result}'"
    print("PASS - test_clean_text_removes_extra_spaces")

def test_clean_text_strips_whitespace():
    result = clean_text("  hello world  ")
    assert result == "hello world", f"Expected 'hello world' but got '{result}'"
    print("PASS - test_clean_text_strips_whitespace")

def test_clean_text_limits_length():
    long_text = "a" * 600
    result = clean_text(long_text)
    assert len(result) <= 504, f"Expected max 504 chars but got {len(result)}"
    print("PASS - test_clean_text_limits_length")

def test_clean_text_handles_empty():
    result = clean_text("")
    assert result == "", f"Expected empty string but got '{result}'"
    print("PASS - test_clean_text_handles_empty")

def test_clean_text_handles_none():
    result = clean_text(None)
    assert result == "", f"Expected empty string but got '{result}'"
    print("PASS - test_clean_text_handles_none")

# ---- test remove_nulls ----

def test_remove_nulls_removes_missing_review():
    reviews = [
        {'id': '1', 'product_id': 'A1', 'review': 'Great product'},
        {'id': '2', 'product_id': 'A2', 'review': ''},     # empty review
        {'id': None, 'product_id': 'A3', 'review': 'Good'}, # null id
    ]
    result = remove_nulls(reviews)
    assert len(result) == 1, f"Expected 1 review but got {len(result)}"
    print("PASS - test_remove_nulls_removes_missing_review")

# ---- test remove_duplicates ----

def test_remove_duplicates_removes_duplicate():
    reviews = [
        {'id': '1', 'product_id': 'A1', 'review': 'Great product, fast delivery'},
        {'id': '2', 'product_id': 'A2', 'review': 'Great product, fast delivery'},
        {'id': '3', 'product_id': 'A3', 'review': 'Terrible quality, broke after one week'},
    ]
    result = remove_duplicates(reviews)
    assert len(result) == 2, f"Expected 2 reviews but got {len(result)}"
    print("PASS - test_remove_duplicates_removes_duplicate")

# ---- test remove_empty ----

def test_remove_empty_removes_blank_review():
    reviews = [
        {'id': '1', 'product_id': 'A1', 'review': 'Great product'},
        {'id': '2', 'product_id': 'A2', 'review': '   '},
        {'id': '3', 'product_id': 'A3', 'review': ''},
    ]
    result = remove_empty(reviews)
    assert len(result) == 1, f"Expected 1 review but got {len(result)}"
    print("PASS - test_remove_empty_removes_blank_review")

# ---- run all tests ----

if __name__ == "__main__":
    print("\n--- Running tests ---\n")
    
    test_clean_text_removes_extra_spaces()
    test_clean_text_strips_whitespace()
    test_clean_text_limits_length()
    test_clean_text_handles_empty()
    test_clean_text_handles_none()
    test_remove_nulls_removes_missing_review()
    test_remove_duplicates_removes_duplicate()
    test_remove_empty_removes_blank_review()
    
    print("\n--- All tests passed ---")