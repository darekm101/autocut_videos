import os
import json
import glob

def generate_video_cuts(configs):
    print(f"generate_video_cuts()")
    print(f"Processing video files in directory: {configs['source_video_files']}")
    print(f"Processing audio meta files in directory: {configs['temp_audio_configs']}")

    min_clip_duration = configs.get('minimum_clip_duration', 2)

    # List all files in the directory
    # all_files = glob.glob(os.path.join(configs['source_video_files'], '*'))
    all_files = glob.glob(os.path.join(configs['source_video_files'], '**', '*'), recursive=True)

    # Filter for .mp4 and .mov files only
    video_files = [f for f in all_files if f.lower().endswith(('.mp4', '.mov'))]
    video_files.sort()  # Sort the video files

    print(f"Sorted video files: {video_files}")

    audio_meta_files = [f for f in os.listdir(configs['temp_audio_configs']) if f.endswith(".json")]
    print(f"Audio meta files: {audio_meta_files}")

    total_duration = 0

    print(f"audio_meta_files: {audio_meta_files}")

    for file_name in audio_meta_files:
        audio_meta_path = os.path.join(configs['temp_audio_configs'], file_name)

        with open(audio_meta_path, "r") as json_file:
            json_data = json.load(json_file)
            print(f"Loaded JSON data from: {audio_meta_path}")

            # Create a new list to hold the updated json data
            new_json_data = []

            
            for i in range(min(len(json_data), len(video_files))):
                if json_data[i]["video_cut_point"] == True: 

                    json_data[i]["duration_from_last_video_cut_point"] *= min_clip_duration
                    
                    json_data[i]["source_video"] = video_files[i]
                    total_duration += json_data[i]["duration_from_last_video_cut_point"]
                    print(f"Assigning source video {video_files[i]} to sequence number {json_data[i]['video_sequence_id']}")
                    new_json_data.append(json_data[i])
                else: 
                    continue

            trailer_file_name = os.path.splitext(file_name)[0] + "-trailer.json"
            trailer_path = os.path.join(configs['temp_video_configs'], trailer_file_name)

            os.makedirs(os.path.dirname(trailer_path), exist_ok=True)

            # Get source audio file name
            source_audio_file = os.path.splitext(file_name)[0] + ".mp3"

            with open(trailer_path, "w") as trailer_file:
                trailer_meta = {
                    "trailer_duration": total_duration,
                    "source_audio_file": source_audio_file,  # Add source audio filename to trailer metadata
                    "clips": new_json_data
                }
                json.dump(trailer_meta, trailer_file, indent=4)
                print(f"Generated trailer JSON file: {trailer_path}")

if __name__ == "__main__":
    import read_configs
    configs = read_configs.read_environment()
    generate_video_cuts(configs)
