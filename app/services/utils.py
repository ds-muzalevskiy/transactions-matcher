import re

def extract_name(description: str):
    match = re.search(r'from\s+(.+?)\s+for Deel', description, re.IGNORECASE)
    return match.group(1) if match else None

def clean_description(description: str) -> str:
 
    cleaned = re.sub(r'for Deel', '', description, flags=re.IGNORECASE)
    cleaned = re.sub(r'ref [\w/]+', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()