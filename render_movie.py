import os
import subprocess
import json

def combine_all(config):
    print(f"________ MODULE: render_movie.py ___________")

    # Retrieve configuration values
    temp_videos_directory = os.path.abspath(config['temp_videos'])
    movie_config = config['movie_config']
    output_directory = config['output_directory']
    final_movie_title = config['final_movie_title']

    # Create output directory if not exist
    os.makedirs(output_directory, exist_ok=True)

    # Load movie config
    with open(movie_config, 'r') as json_file:
        movie_config_data = json.load(json_file)

    # Create temporary file list for ffmpeg
    temp_file_list = os.path.join(temp_videos_directory, "temp_file_list.txt")
    with open(temp_file_list, "w") as file:
        for clip in movie_config_data:
            try:
                trimmed_video = clip['source_trimmed_video']
                file.write(f"file '{trimmed_video}'\n")
            except KeyError:
                print(f"source_trimmed_video not found in movie_config_data. Skipping this clip. {clip}")
                continue

    # Output file
    output_file = os.path.join(output_directory, f"{final_movie_title}.mp4")

    # Use ffmpeg to concatenate the video files
    command = f"ffmpeg -f concat -safe 0 -i {temp_file_list} -c copy {output_file}"
    ffmpeg_output = subprocess.run(command, shell=True)

    # Check the return code of FFmpeg command
    if ffmpeg_output.returncode == 0:
        print(f"combine_all(): Final movie saved as {output_file}")
    else:
        print(f"combine_all(): FFmpeg command failed with return code {ffmpeg_output.returncode}")

    # Clean up temporary file
    os.remove(temp_file_list)

if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    combine_all(config)
