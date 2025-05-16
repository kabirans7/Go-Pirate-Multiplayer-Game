# Adapted from utils.py

import re

# Normalize user input for easier matching
def clean_text(text):
    # Lowercase everything
    text = text.lower()
    # Remove extra spaces
    text = text.strip()
    # Remove punctuation (basic)
    text = re.sub(r'[^\w\s]', '', text)
    return text