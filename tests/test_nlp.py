import pytest
from src.nlp_processor import clean_text, rating_to_label

def test_clean_text_lowercasing():
    assert clean_text("EXCELLENT APP") == "excellent app"

def test_clean_text_punctuation_removal():
    assert clean_text("Great service! Very fast, 100% recommended.") == "great service very fast recommended"

def test_clean_text_whitespace():
    assert clean_text("  too   many    spaces  ") == "too many spaces"

def test_rating_to_label_negative():
    assert rating_to_label(1) == "Negative"
    assert rating_to_label(2) == "Negative"

def test_rating_to_label_neutral():
    assert rating_to_label(3) == "Neutral"

def test_rating_to_label_positive():
    assert rating_to_label(4) == "Positive"
    assert rating_to_label(5) == "Positive"
