import os
import json
import librosa
import numpy as np

DB_FILE = "fingerprints.json"

def load_db():
    """Load the fingerprint database from the JSON file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = f.read().strip()
                if not data:
                    return []
                return json.loads(data)
            except json.decoder.JSONDecodeError:
                return []
    else:
        print("Database file not found.")
        return []

def process_file(file_path):
    """
    Process a query audio file to extract its fingerprint.
    Uses the same method as in build_fingerprint_db.py.
    """
    try:
        y, sr = librosa.load(file_path, duration=30)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        mfcc_mean = np.mean(mfcc, axis=1)
        fingerprint = mfcc_mean.tolist()
        return fingerprint, len(y) / sr
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def cosine_similarity(vec1, vec2):
    """Compute the cosine similarity between two vectors."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(v1, v2) / (norm1 * norm2)

def match_query(query_file):
    """
    Compute the query file's fingerprint and compare it to stored fingerprints.
    Returns a list of matching files with cosine similarity scores.
    """
    query_fp, query_duration = process_file(query_file)
    if not query_fp:
        return []
    
    db = load_db()
    results = []
    for entry in db:
        db_fp = entry.get("features")
        sim = cosine_similarity(query_fp, db_fp)
        results.append((entry.get("file_path", "Unknown"), sim))
    
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
