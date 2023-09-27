import argparse
import os

def overlay_audio(mp4_input, mp3_input, mp3_volume=1.0, output_file="movie_final.mp4"):
    # Using ffmpeg to mix MP3 audio with MP4's audio
    cmd = (f'ffmpeg -i {mp4_input} -i {mp3_input} '
           f'-filter_complex "[1:a]volume={mp3_volume}[mp3vol];[0:a][mp3vol]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
           f'-map 0:v -map "[aout]" -c:v copy -c:a aac -strict experimental {output_file}')
    
    os.system(cmd)
    
if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description="Mix MP3 audio onto an MP4 video")
    parser.add_argument("--input-mp4", required=True, help="Input MP4 file")
    parser.add_argument("--input-mp3", required=True, help="Input MP3 file")
    parser.add_argument("--mp3-volume", type=float, default=1.0, help="Volume adjustment for the MP3 file (e.g., 0.5 for half, 1.0 for unchanged, 2.0 for double, etc.)")
    
    args = parser.parse_args()
    
    overlay_audio(args.input_mp4, args.input_mp3, args.mp3_volume)
