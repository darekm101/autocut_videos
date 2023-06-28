import json
import subprocess
import os

def read_json_file(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def combine_all(config_file, video_file):
    # Read the config and video data
    config = read_json_file(config_file)
    video = read_json_file(video_file)

    # Define the output and temporary files
    output_combined_audio_file = os.path.join(config['output_dir'], config['combined_audio_file'])
    temp_combined_video_file = os.path.join(config['temp_dir'], config['combined_video_file'])
    final_movie_file = os.path.join(config['output_dir'], config['final_movie_file'])
    temp_video_files_list = os.path.join(config['temp_dir'], config['video_files_list'])

    # Create a list of video files
    video_files = [os.path.join(config['output_dir'], f) for f in video['files']]
    
    # Write the list of video files to a temporary file
    with open(temp_video_files_list, 'w') as file:
        file.write('\n'.join(f"file '{f}'" for f in video_files))

    try:
        # Concatenate all the video files
        command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_video_files_list, '-c', 'copy', temp_combined_video_file]
        subprocess.run(command, check=True)

        # Merge the combined video file and the audio file
        command = ['ffmpeg', '-i', temp_combined_video_file, '-i', output_combined_audio_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', final_movie_file]
        subprocess.run(command, check=True)

        print(f"combine_all(): Final movie created and saved as {final_movie_file}")
    except subprocess.CalledProcessError:
        print("Error encountered while creating the movie. Please check the ffmpeg commands and inputs.")

if __name__ == "__main__":
    combine_all('config.json', 'video.json')

