import os
import json
import librosa
import numpy as np

DB_FILE = "fingerprints.json"

def load_db():
    """Load the fingerprint database from a JSON file."""
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
        return []

def save_db(db):
    """Save the fingerprint database to a JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def process_file(file_path):
    """
    Process an audio file to extract a rich fingerprint.
    This version uses librosa to compute a mean MFCC vector (20 coefficients).
    """
    try:
        # Load the audio (first 30 seconds for speed)
        y, sr = librosa.load(file_path, duration=30)
        # Compute 20 MFCC coefficients
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        # Compute the mean value for each coefficient over time
        mfcc_mean = np.mean(mfcc, axis=1)
        # Convert the numpy array to a list for JSON serialization
        fingerprint = mfcc_mean.tolist()
        return {
            "file_path": file_path,
            "features": fingerprint,
            "duration": len(y) / sr
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def add_file_to_db(file_path):
    """Process a file and add its fingerprint to the database."""
    db = load_db()
    entry = process_file(file_path)
    if entry:
        db.append(entry)
        save_db(db)
        print(f"Added fingerprint for {file_path}")
    else:
        print(f"Failed to add fingerprint for {file_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python build_fingerprint_db.py <file_or_directory>")
        exit(1)
    
    path = sys.argv[1]
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith((".mp3", ".wav", ".flac")):
                    full_path = os.path.join(root, file)
                    add_file_to_db(full_path)
    else:
        add_file_to_db(path)
