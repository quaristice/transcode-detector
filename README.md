# transcode-detector

A Python script that detects transcoded FLAC files.

## Installation
Install dependencies (And Python 3, of course).

`pip install -r requirements.txt`

Optional: Move script into your music folder.

## Usage
In the terminal:
`python3 transcode-detector.py [music-folder-path]`

If the music folder path is not specified, the script uses the directory it is in as the working directory.

The script will recursively traverse through the folder, and print out the path of any FLAC it detects to be a bad transcode.
