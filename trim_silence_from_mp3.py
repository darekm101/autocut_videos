import os
import argparse
from pydub import AudioSegment

parser = argparse.ArgumentParser(description='Process mp3 files.')
parser.add_argument('dirpath', type=str, help='Directory path to process')
args = parser.parse_args()

input_dir = args.dirpath

for dirpath, dirnames, filenames in os.walk(input_dir):
    mp3_files = [f for f in filenames if f.lower().endswith('.mp3')]
    
    for mp3_file in mp3_files:
        full_path = os.path.join(dirpath, mp3_file)
        print("Processing file:", full_path)
        
        audio = AudioSegment.from_mp3(full_path)
        print("Loaded audio file.")

        trimmed_audio = audio.strip_silence(silence_thresh=-40, padding=500)
        print("Trimmed silence from audio file with silence threshold -40 dBFS and padding of 100 ms.")

        trimmed_audio.export(full_path, format="mp3")
        print("Saved trimmed audio file.")

print("All mp3 files have been trimmed!")

