import os
import json
import librosa

def write_json(config):
    print(f"________ MODULE: make_initial_cutlist.py ___________")

    source_audio_directory = config['source_audio_files']
    temp_directory = config['temp_directory']
    min_clip_duration = config["minimum_clip_duration"]
    initial_cut_list_file = config['initial_cutlist']
    initial_cut_list = initial_cut_list_file

    # Create the temp directory if it doesn't exist
    os.makedirs(temp_directory, exist_ok=True)

    # Get a list of all audio files in the source directory
    audio_files = [f for f in os.listdir(source_audio_directory) if f.endswith('.mp3')]

    # Generate beats and cut points for each audio file
    all_cut_points = []
    video_sequence_id = 1
    for file_name in audio_files:
        audio_path = os.path.join(source_audio_directory, file_name)
        y, sr = librosa.load(audio_path)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        sequence_number = 1
        video_clip_duration = 0

        for i in range(len(beat_frames)):
            if i == 0:
                duration_from_last = librosa.frames_to_time(beat_frames[i], sr=sr)
            else:
                duration_from_last = librosa.frames_to_time(beat_frames[i] - beat_frames[i - 1], sr=sr)

            video_clip_duration += duration_from_last

            item = {
                "sequence_number": sequence_number,
                "duration_from_last": duration_from_last,
                "video_sequence_id": video_sequence_id
            }

            if video_clip_duration >= min_clip_duration:
                item["video_cut_point"] = True
                item["duration_from_last_video_cut_point"] = video_clip_duration
                video_clip_duration = 0
                video_sequence_id += 1
            else:
                item["video_cut_point"] = False

            all_cut_points.append(item)

            sequence_number += 1

    # Write the cut points to the initial cut list file
    with open(initial_cut_list, "w") as json_file:
        json.dump(all_cut_points, json_file, indent=4)

    print(f"write_json(): Initial cut list written to {initial_cut_list}")

if __name__ == '__main__':
    # Test the function
    import read_config
    config = read_config.read_json()
    write_json(config)
