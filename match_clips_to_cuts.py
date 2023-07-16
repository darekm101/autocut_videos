import os
import glob
import json
import random
import subprocess

def get_video_files(config):
    video_files_directory = os.path.abspath(config['source_video_files'])
    all_files = glob.glob(os.path.join(video_files_directory, '**', '*'), recursive=True)
    video_files = [f for f in all_files if f.lower().endswith(('.mp4', '.mov'))]
    video_files.sort()
    return video_files

def get_video_duration(video_path):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    return float(subprocess.check_output(command))

def validate_video_files(video_files, min_clip_duration):
    print(f"________ MODULE: match_clips_to_cuts.py - validate_video_files() ___________")
    valid_video_files = []
    for video_file in video_files:
        video_duration = get_video_duration(video_file)
        if video_duration < min_clip_duration:
            print(f"Skipping video {video_file} because it is shorter {video_duration} than minimum clip duration {min_clip_duration}")
        else:
            valid_video_files.append(video_file)
    print(f"validate_video_files(): Remaining valid clips: {len(valid_video_files)}")
    return valid_video_files

def get_random_start_time(clip, min_clip_duration):
    print(f"________ MODULE: match_clips_to_cuts.py - get_random_start_time() ___________")
    
    source_video_duration = clip["source_video_duration"]
    print(f"get_random_start_time(): source_video_duration - {source_video_duration} seconds")

    max_start_time = source_video_duration - min_clip_duration
    print(f"get_random_start_time(): Maximum valid start time - {max_start_time} seconds")

    if max_start_time < 0:
        print(f"get_random_start_time(): Clip duration is less than minimum clip duration for {clip['source_video']}")
        return None

    start_time = random.uniform(0, max_start_time)
    print(f"get_random_start_time(): Random start time - {start_time} seconds")

    hours = int(start_time // 3600)
    minutes = int((start_time % 3600) // 60)
    seconds = start_time % 60
    formatted_start_time = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

    print(f"get_random_start_time(): Generated random start time for clip {clip['source_video']} - {formatted_start_time}")

    return formatted_start_time




def assign_clips(config):
    print(f"________ MODULE: match_clips_to_cuts.py - assign_clips() ___________")
    min_clip_duration = config["minimum_clip_duration"]
    video_files = get_video_files(config)
    valid_video_files = validate_video_files(video_files, min_clip_duration)
    movie_config = config['movie_config']

    with open(movie_config, "r") as json_file:
        movie_clips = json.load(json_file)

    for idx, valid_video in enumerate(valid_video_files):
        if idx < len(movie_clips):
            movie_clips[idx]["source_video"] = valid_video
            movie_clips[idx]["source_video_duration"] = get_video_duration(valid_video)
            movie_clips[idx]["clip_starttime"] = get_random_start_time(movie_clips[idx], min_clip_duration)

    with open(movie_config, "w") as json_file:
        json.dump(movie_clips, json_file, indent=4)

    print(f"assign_clips(): Assigned source videos and their durations to movie.json")


if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    assign_clips(config)
