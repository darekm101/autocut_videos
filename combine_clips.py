import os
import json
import subprocess
import tempfile

def combine_clips(configs):

    line_break = "*" * 50
    print(f"Running combine_clips(){line_break}")

    # Ensure the output directory exists
    output_directory = configs["output_directory"]
    os.makedirs(output_directory, exist_ok=True)

    # Location of video configurations
    video_configs_directory = configs["temp_video_configs"]

    # Location of temporary audio files
    temp_audio_directory = configs["temp_audios"]

    # Read all JSON files in the directory
    video_config_files = [f for f in os.listdir(video_configs_directory) if f.endswith(".json")]

    for file_name in video_config_files:
        video_config_path = os.path.join(video_configs_directory, file_name)

        with open(video_config_path, 'r') as json_file:
            video_configs = json.load(json_file)

            # Array to store clip file paths
            clips = []

            # Loop over each clip configuration
            for clip in video_configs["clips"]:
                # Add each source video path to the clips list
                clips.append(os.path.join(os.getcwd(), clip["source_trimmed_video"]))  # Use absolute paths

            # Create a temporary file for ffmpeg to write the file paths
            with tempfile.NamedTemporaryFile(dir=configs["temp_directory"], delete=False) as f:
                for clip in clips:
                    f.write(f'file \'{clip}\'\n'.encode())

            # Construct the name of the output file
            output_file = os.path.join(configs["output_directory"], f'{file_name.split(".")[0]}_combined.mp4')

            # Run ffmpeg to concatenate the videos. 
            # -f concat: specifies that we are providing a list of files to concatenate
            # -safe 0: allows us to use absolute file paths
            # -i: input file path
            # -c copy: copies the first video stream and the first audio stream from each file
            subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f.name, '-c', 'copy', output_file])

            # Run ffmpeg to add the audio to the video.
            # The source audio file path is assumed to be the same name as the video_config file but in the temp_audios directory
            audio_file_path = os.path.join(temp_audio_directory, f'{file_name.split(".")[0]}.mp3')
            output_with_audio = os.path.join(configs["output_directory"], f'{file_name.split(".")[0]}_final.mp4')

            # The -shortest command is used to ensure the audio matches the length of the video
            subprocess.run(['ffmpeg', '-y', '-i', output_file, '-i', audio_file_path, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_with_audio])

            print(f"Generated combined video: {output_with_audio}")


if __name__ == "__main__":
    import read_configs
    configs = read_configs.read_environment()

    combine_clips(configs)
