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

## How It Works

1. **Fingerprint Generation:**
   - The system loads an audio file and computes its spectrogram.
   - It detects local spectral peaks (landmarks) in the spectrogram.
   - By pairing nearby peaks (with defined time differences), the system creates compact fingerprint hashes.

2. **Database Storage:**
   - Fingerprints, along with metadata (e.g., file path, duration), are stored in a JSON file (`fingerprints.json`).
   - New fingerprints are appended to the database for future matching.

3. **Query Matching:**
   - For a query audio file, the system computes its fingerprint using the same process.
   - It compares the query fingerprint with the stored database fingerprints using a simple Jaccard similarity measure (by converting fingerprints into sets of numbers).
   - Matching songs are ranked and displayed based on the count of matching fingerprint hashes.

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
```

## Usage

### 1. Build the Fingerprint Database

Run the `build_fingerprint_db.py` script to process audio files from a given file or directory. This script computes fingerprints for all supported audio files (e.g., MP3, WAV, FLAC) and appends them to `fingerprints.json`.

**Example:**

```bash
python build_fingerprint_db.py /path/to/your/music_directory
```

To process a single file:

```bash
python build_fingerprint_db.py /path/to/your/audio_file.mp3
```

### 2. Match a Query Audio File

Use the `match_fingerprint.py` script to match a query audio file against the stored fingerprints. The script will output a list of matching files with similarity scores.

**Example:**

```bash
python match_fingerprint.py /path/to/query_song.mp3
```

The output will display the file paths along with a similarity score for each matching entry.

## Extending the Project

- **AcoustID Lookup:**  
  You can integrate AcoustID's online lookup service (requires an API key) to fetch additional metadata such as song title and artist.
- **Improved Matching Algorithms:**  
  Enhance the matching process by including time offset alignment or more advanced similarity metrics.
- **User Interface:**  
  Consider building a GUI or a web-based interface for easier interaction with the system.

## Troubleshooting

- **Fingerprint Extraction Errors:**  
  Ensure that your audio files are in a supported format and that Chromaprint is correctly installed.
- **Dependency Issues:**  
  If you encounter problems with the `pyacoustid` package, consult its [GitHub repository](https://github.com/beetbox/pyacoustid) for further assistance.
