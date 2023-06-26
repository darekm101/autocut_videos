import os
import json
import subprocess

def trim_audio(configs):
    print("Trim_audio()")

    # Location of video configurations
    video_configs_directory = configs["temp_video_configs"]

    # Location of source audio files
    source_audio_directory = configs["source_audio_files"]

    # Location of temporary audio files
    temp_audio_directory = configs["temp_audios"]

    # Ensure the temp audio directory exists
    os.makedirs(temp_audio_directory, exist_ok=True)

    # Read all JSON files in the directory
    video_config_files = [f for f in os.listdir(video_configs_directory) if f.endswith(".json")]

    for file_name in video_config_files:
        video_config_path = os.path.join(video_configs_directory, file_name)

        with open(video_config_path, 'r') as json_file:
            video_configs = json.load(json_file)

            # Duration of the video
            video_duration = video_configs["trailer_duration"]

            # Audio file path is based on the "source_audio_file" key in video_configs
            source_audio_file = video_configs['source_audio_file']
            audio_file_path = os.path.join(source_audio_directory, source_audio_file)

            # Construct the name of the output file
            output_file = os.path.join(temp_audio_directory, f'{file_name.split(".")[0]}.mp3')

            # Run ffmpeg to trim the audio to match the video duration. -t specifies the duration.
            subprocess.run(['ffmpeg', '-y', '-i', audio_file_path, '-t', str(video_duration), '-c:a', 'copy', output_file])

            print(f"Generated trimmed audio file: {output_file}")


if __name__ == "__main__":
    import read_configs
    configs = read_configs.read_environment()
    trim_audio(configs)