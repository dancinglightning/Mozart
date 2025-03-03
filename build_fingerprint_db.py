# build_fingerprint_db.py

import os
import json
import acoustid

DB_FILE = "fingerprints.json"

def load_db():
    """Load the fingerprint database from a JSON file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def save_db(db):
    """Save the fingerprint database to a JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def process_file(file_path):
    """
    Generate a fingerprint for the audio file using the AcoustID library.
    Returns a dictionary with the file path, fingerprint, and duration.
    """
    try:
        fingerprint, duration = acoustid.fingerprint_file(file_path)
        return {
            "file_path": file_path,
            "fingerprint": fingerprint,
            "duration": duration
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
        # Process all supported audio files in the directory and subdirectories.
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith((".mp3", ".wav", ".flac")):
                    full_path = os.path.join(root, file)
                    add_file_to_db(full_path)
    else:
        add_file_to_db(path)
