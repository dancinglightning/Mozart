# match_fingerprint.py

import os
import json
import acoustid

DB_FILE = "fingerprints.json"

def load_db():
    """Load the fingerprint database from the JSON file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        print("Database file not found.")
        return []

def process_file(file_path):
    """
    Generate a fingerprint for the query audio file.
    Returns the fingerprint string and duration.
    """
    try:
        fingerprint, duration = acoustid.fingerprint_file(file_path)
        return fingerprint, duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def fingerprint_to_set(fingerprint):
    """
    Convert the fingerprint (a string of numbers separated by commas or spaces)
    to a set of integers for simple similarity computation.
    """
    try:
        if "," in fingerprint:
            numbers = [int(x) for x in fingerprint.split(",") if x.strip().isdigit()]
        else:
            numbers = [int(x) for x in fingerprint.split() if x.strip().isdigit()]
        return set(numbers)
    except Exception as e:
        print("Error converting fingerprint to set:", e)
        return set()

def jaccard_similarity(set1, set2):
    """Compute the Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def match_query(query_file):
    """
    Compute the query file fingerprint, compare it to the stored fingerprints,
    and return a list of matching files along with their similarity scores.
    """
    query_fp, query_duration = process_file(query_file)
    if not query_fp:
        return []
    
    query_set = fingerprint_to_set(query_fp)
    db = load_db()
    
    results = []
    for entry in db:
        db_fp = entry["fingerprint"]
        db_set = fingerprint_to_set(db_fp)
        similarity = jaccard_similarity(query_set, db_set)
        results.append((entry["file_path"], similarity))
    
    # Sort results by similarity (highest first)
    results.sort(key=lambda x: x[1], reverse=True)
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python match_fingerprint.py <query_file>")
        exit(1)
    
    query_file = sys.argv[1]
    matches = match_query(query_file)
    if matches:
        print("Matches:")
        for file_path, score in matches:
            print(f"{file_path}: {score:.2f}")
    else:
        print("No matches found.")
