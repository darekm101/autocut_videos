import os
import json
import glob
from moviepy.editor import VideoFileClip
import read_configs

def get_video_files(configs):
    all_files = glob.glob(os.path.join(configs['source_video_files'], '**', '*'), recursive=True)
    video_files = [f for f in all_files if f.lower().endswith(('.mp4', '.mov'))]
    video_files.sort() 
    return video_files

def get_audio_meta_files(configs):
    audio_meta_files = [f for f in os.listdir(configs['temp_audio_configs']) if f.endswith(".json")]
    return audio_meta_files

def process_audio_meta_files(audio_meta_files, video_files, configs, min_clip_duration):
    total_duration = 0
    for file_name in audio_meta_files:
        audio_meta_path = os.path.join(configs['temp_audio_configs'], file_name)
        with open(audio_meta_path, "r") as json_file:
            json_data = json.load(json_file)
            new_json_data, total_duration = process_single_audio_meta(json_data, video_files, total_duration, min_clip_duration)
            generate_trailer_json(file_name, new_json_data, total_duration, configs)

def process_single_audio_meta(json_data, video_files, total_duration, min_clip_duration):
    new_json_data = []
    sum_duration_from_last = 0
    for i in range(min(len(json_data), len(video_files))):
        video_file = video_files[i]
        video = VideoFileClip(video_file)
        if video.duration < min_clip_duration:
            print(f"Skipping video {video_file} because it is shorter {video.duration} than minimum clip duration {min_clip_duration}")
            continue
        sum_duration_from_last += json_data[i]["duration_from_last"]
        if json_data[i]["video_cut_point"] == True: 
            json_data[i]["duration_from_last_video_cut_point"] = sum_duration_from_last
            sum_duration_from_last = 0  # Reset sum
            json_data[i]["source_video"] = video_files[i]
            total_duration += json_data[i]["duration_from_last_video_cut_point"]
            new_json_data.append(json_data[i])
    return new_json_data, total_duration

def generate_trailer_json(file_name, new_json_data, total_duration, configs):
    trailer_file_name = os.path.splitext(file_name)[0] + "-trailer.json"
    trailer_path = os.path.join(configs['temp_video_configs'], trailer_file_name)
    os.makedirs(os.path.dirname(trailer_path), exist_ok=True)
    source_audio_file = os.path.splitext(file_name)[0] + ".mp3"
    with open(trailer_path, "w") as trailer_file:
        trailer_meta = {
            "trailer_duration": total_duration,
            "source_audio_file": source_audio_file,  
            "clips": new_json_data
        }
        json.dump(trailer_meta, trailer_file, indent=4)

def generate_video_cuts(configs):
    min_clip_duration = configs['minimum_clip_duration']
    video_files = get_video_files(configs)
    audio_meta_files = get_audio_meta_files(configs)
    process_audio_meta_files(audio_meta_files, video_files, configs, min_clip_duration)

if __name__ == "__main__":
    configs = read_configs.read_environment()
    generate_video_cuts(configs)


# import os
# import json
# import glob
# import pdb

# def generate_video_cuts(configs):
#     print(f"generate_video_cuts()")
#     print(f"Processing video files in directory: {configs['source_video_files']}")
#     print(f"Processing audio meta files in directory: {configs['temp_audio_configs']}")

#     min_clip_duration = configs['minimum_clip_duration']

#     all_files = glob.glob(os.path.join(configs['source_video_files'], '**', '*'), recursive=True)

#     video_files = [f for f in all_files if f.lower().endswith(('.mp4', '.mov'))]
#     video_files.sort()  

#     print(f"Sorted video files: {video_files}")
#     print(f"Number of video files: {len(video_files)}")

#     audio_meta_files = [f for f in os.listdir(configs['temp_audio_configs']) if f.endswith(".json")]
#     print(f"Audio meta files: {audio_meta_files}")

#     total_duration = 0

#     print(f"audio_meta_files: {audio_meta_files}")

#     for file_name in audio_meta_files:
#         audio_meta_path = os.path.join(configs['temp_audio_configs'], file_name)

#         with open(audio_meta_path, "r") as json_file:
#             json_data = json.load(json_file)
#             print(f"Loaded JSON data from: {audio_meta_path}")

#             new_json_data = []
#             sum_duration_from_last = 0

#             for i in range(min(len(json_data), len(video_files))):
#                 sum_duration_from_last += json_data[i]["duration_from_last"]

#                 if json_data[i]["video_cut_point"] == True: 
#                     json_data[i]["duration_from_last_video_cut_point"] = sum_duration_from_last
#                     sum_duration_from_last = 0  # Reset sum

#                     json_data[i]["source_video"] = video_files[i]
#                     total_duration += json_data[i]["duration_from_last_video_cut_point"]
#                     print(f"Assigning source video {video_files[i]} to sequence number {json_data[i]['video_sequence_id']}")
#                     new_json_data.append(json_data[i])

#             trailer_file_name = os.path.splitext(file_name)[0] + "-trailer.json"
#             trailer_path = os.path.join(configs['temp_video_configs'], trailer_file_name)

#             os.makedirs(os.path.dirname(trailer_path), exist_ok=True)

#             source_audio_file = os.path.splitext(file_name)[0] + ".mp3"

#             with open(trailer_path, "w") as trailer_file:
#                 trailer_meta = {
#                     "trailer_duration": total_duration,
#                     "source_audio_file": source_audio_file,  
#                     "clips": new_json_data
#                 }
#                 json.dump(trailer_meta, trailer_file, indent=4)
#                 print(f"Generated trailer JSON file: {trailer_path}")

# if __name__ == "__main__":
#     import read_configs
#     configs = read_configs.read_environment()
#     generate_video_cuts(configs)
