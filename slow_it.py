import argparse
import subprocess
import json
import os
import fnmatch
from pathlib import Path
from datetime import datetime
import re

def probe_file(file):
    command = ["ffprobe", "-loglevel", "quiet", "-print_format", "json", "-show_format", "-show_streams", "-i", file]
    output = subprocess.run(command, capture_output=True, text=True).stdout
    return json.loads(output)

def get_metadata_creation_time(metadata):
    if 'tags' in metadata:
        tags = metadata['tags']
        if 'creation_time' in tags:
            creation_time_str = tags['creation_time']
            # Example: '2020-06-12T19:20:14.000000Z'
            dt = datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            timestamp = dt.timestamp()
            return timestamp
    return None

def find_files(directory, pattern):
    for path in Path(directory).rglob('*'):
        if fnmatch.fnmatchcase(path.name, pattern):
            yield str(path)

parser = argparse.ArgumentParser(description='Slow down video files.')
parser.add_argument('--input-dir', type=str, help='Input directory', required=True)
parser.add_argument('--output-dir', type=str, help='Output directory', default='output')
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Supported movie file extensions
extensions = ('*.mp4', '*.MP4', '*.mkv', '*.MKV', '*.avi', '*.AVI', '*.mov', '*.MOV', '*.flv', '*.FLV')

for extension in extensions:
    for input_file in find_files(input_dir, extension):
        print("Processing file:", input_file)

        output_file = os.path.join(output_dir, os.path.basename(input_file))
        
        probe_data = probe_file(input_file)
        video_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'video']

        if video_streams:
            video_stream = video_streams[0]
            codec_name = video_stream.get('codec_name')
            print("Video codec:", codec_name)

            pix_fmt = video_stream.get('pix_fmt')
            print("Pixel format:", pix_fmt)

            bit_rate = video_stream.get('bit_rate')
            print("Bit rate:", bit_rate)
            
            # Retrieve the original frame rate
            r_frame_rate = video_stream.get('avg_frame_rate')
            frame_rate = eval(r_frame_rate) # r_frame_rate is a string like '24000/1001', this will calculate it to a float
            new_frame_rate = frame_rate / 2 # Halve the frame rate

            # Copy over the metadata creation_time
            orig_creation_timestamp = get_metadata_creation_time(probe_data['format'])
            if orig_creation_timestamp is not None:
                command = f'ffmpeg -i {input_file} -filter:v "setpts=2.0*PTS" -r {new_frame_rate} -c:v {codec_name} -tag:v hvc1 -pix_fmt {pix_fmt} -b:v {bit_rate} -map_metadata 0 -metadata creation_time={datetime.utcfromtimestamp(orig_creation_timestamp).isoformat()} {output_file}'
            else:
                command = f'ffmpeg -i {input_file} -filter:v "setpts=2.0*PTS" -r {new_frame_rate} -c:v {codec_name} -tag:v hvc1 -pix_fmt {pix_fmt} -b:v {bit_rate} -map_metadata 0 {output_file}'

            subprocess.call(command, shell=True)

            print(f"Slowed down the video by reducing the frame rate from {frame_rate} to {new_frame_rate}.")
            print("Saved slowed down video file.")
        else:
            print(f"No video streams found in {input_file}.")

print("All files have been processed!")

