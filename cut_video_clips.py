import os
import json
import subprocess

def cut_video_clips(config):
    print(f"________ MODULE: cut_video_clips.py ___________")

    temp_videos_directory = os.path.abspath(config['temp_videos'])
    movie_config = config['movie_config']

    # Create temp videos directory if not exist
    os.makedirs(temp_videos_directory, exist_ok=True)

    # Load movie config
    with open(movie_config, 'r') as json_file:
        movie_config_data = json.load(json_file)

    for idx, clip in enumerate(movie_config_data):
        try:
            source_video = clip['source_video']
            duration = clip['clip_duration']
            start_time = clip['clip_starttime']
        except KeyError as e:
            print(f"Skipping clip {idx} due to missing key: {e}")
            continue

        # Get the total video length first
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', source_video]
        total_video_length = float(subprocess.check_output(command).decode('utf-8').strip())

        # Ensure that we don't exceed the total video length
        if duration > total_video_length:
            print(f"Skipping {source_video} due to insufficient length")
            continue

        # Get extension of source video
        source_ext = os.path.splitext(source_video)[1]

        # ffmpeg command to cut video without transcodeing, but can cause jitter in video
        output_file = os.path.join(temp_videos_directory, f"{os.path.basename(source_video)}-clip-{idx}.{source_ext}")
        clip['source_trimmed_video'] = output_file
        # command = ['ffmpeg', '-y', '-ss', '0', '-i', source_video, '-t', str(duration), '-c', 'copy', output_file]
        command = ['ffmpeg', '-y', '-ss', start_time, '-i', source_video, '-t', str(duration), '-c', 'copy', output_file]
   
        #Code from Claude
        try:
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"ERROR::Skipping File {source_video} due to error: {e}")
            continue



    # Overwrite the movie config file with updated data
    with open(movie_config, 'w') as json_file:
        json.dump(movie_config_data, json_file, indent=4)
        print(f"cut_video_clips(): Updated movie.json with source trimmed video paths")

if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    cut_video_clips(config)
