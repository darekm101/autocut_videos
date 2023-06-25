import os
import random
import time
import json
import subprocess

def cut_video_clips(configs):
    print(f"cut_video_clips()")
    print(f"Processing video configs in directory: {configs['temp_video_configs']}")

    # Create temp videos directory if not exist
    os.makedirs(configs['temp_videos'], exist_ok=True)

    # Read video config files
    video_config_files = [f for f in os.listdir(configs['temp_video_configs']) if f.endswith(".json")]
    
    for config_file in video_config_files:
        config_file_path = os.path.join(configs['temp_video_configs'], config_file)
        with open(config_file_path, 'r') as json_file:
            video_configs = json.load(json_file)
            clips = video_configs['clips']

            for i, clip in enumerate(clips):
                source_video = clip['source_video']
                duration = clip['duration_from_last_video_cut_point']

                # Get the total video length first
                video_length_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', source_video]
                total_video_length = float(subprocess.check_output(video_length_command).decode('utf-8').strip())
                
                # Get random start time, ensuring it is less than the end time
                start_time = random.uniform(0, max(0, total_video_length - duration))

                # Generate output video file path
                output_file = os.path.join(configs['temp_videos'], f"{os.path.basename(source_video)}-clip-{i}.mp4")
                clip['source_trimmed_video'] = output_file

                # ffmpeg command to cut video without transcoding
                command = [
                    'ffmpeg', '-y', '-i', source_video, '-ss', str(start_time), '-t', str(duration),
                    '-c', 'copy', output_file
                ]
                
                # Run ffmpeg command
                subprocess.run(command, check=True)
        
        # Overwrite the video config file with updated data
        with open(config_file_path, 'w') as json_file:
            json.dump(video_configs, json_file, indent=4)
            print(f"Updated video config file: {config_file_path}")



# import os
# import json
# import subprocess

# def cut_video_clips(configs):
#     print(f"cut_video_clips()")
#     print(f"Processing video configs in directory: {configs['temp_video_configs']}")

#     # Create temp videos directory if not exist
#     os.makedirs(configs['temp_videos'], exist_ok=True)

#     # Read video config files
#     video_config_files = [f for f in os.listdir(configs['temp_video_configs']) if f.endswith(".json")]
    
#     for config_file in video_config_files:
#         config_file_path = os.path.join(configs['temp_video_configs'], config_file)
#         with open(config_file_path, 'r') as json_file:
#             video_configs = json.load(json_file)
#             clips = video_configs['clips']

#             for i, clip in enumerate(clips):
#                 source_video = clip['source_video']
#                 duration = clip['duration_from_last_video_cut_point']

#                 # Generate output video file path
#                 output_file = os.path.join(configs['temp_videos'], f"{os.path.basename(source_video)}-clip-{i}.mp4")
#                 clip['source_trimmed_video'] = output_file

#                 # ffmpeg command to cut video without transcoding
#                 command = [
#                     'ffmpeg', '-y', '-i', source_video, '-ss', '0', '-t', str(duration),
#                     '-c', 'copy', output_file
#                 ]
                
#                 # Run ffmpeg command
#                 subprocess.run(command, check=True)
        
#         # Overwrite the video config file with updated data
#         with open(config_file_path, 'w') as json_file:
#             json.dump(video_configs, json_file, indent=4)
#             print(f"Updated video config file: {config_file_path}")