# Mozart, The Music Recommender

This project implements a simplified audio fingerprinting system inspired by services like Shazam. It consists of two Python scripts:
- **build_fingerprint_db.py**: Processes audio files to generate and store fingerprints in a local JSON database.
- **match_fingerprint.py**: Matches a query audio file against the stored fingerprints to find similar songs.

## Overview

The system uses the Chromaprint/AcoustID library (via the `pyacoustid` package) to compute audio fingerprints for music files. It then:
1. **Fingerprint Generation and Storage:**
   - Loads an audio file and computes its fingerprint.
   - Stores the fingerprint (along with file metadata) in a local JSON file (`fingerprints.json`), appending new entries.
2. **Matching Query Audio:**
   - Computes the fingerprint for a query audio file.
   - Loads stored fingerprints from `fingerprints.json`.
   - Compares the query fingerprint against the database using a simple Jaccard similarity measure.
   - Returns a ranked list of matching songs based on similarity scores.

## Installation

### Prerequisites

- **Python 3.6+**  
  Download and install from [python.org](https://www.python.org/downloads/).

- **Chromaprint**  
  Required for fingerprint extraction.
  - **Windows:** Download and install the Chromaprint binaries from [AcoustID](https://acoustid.org/chromaprint).
  - **macOS:** Install via Homebrew:
    ```bash
    brew install chromaprint
    ```
  - **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt-get install libchromaprint-tools
    ```

### Python Dependencies

It is recommended to use a virtual environment. Then install the required packages using the provided `requirements.txt` file:

```bash
python -m venv venv
source venv/bin/activate         # On Linux/MacOS
venv\Scripts\activate            # On Windows

pip install -r requirements.txt
