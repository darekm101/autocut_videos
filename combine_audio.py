import os
import subprocess

def combine_audio(config):
    print(f"________ MODULE: combine_audio.py ___________")

    source_audio_directory = os.path.abspath(config['source_audio_files'])
    temp_directory = os.path.abspath(config['temp_directory'])
    final_audio_name = config['final_movie_title'] + '.mp3'
    output_audio_file = os.path.join(temp_directory, final_audio_name)

    # Create the temp directory if it doesn't exist
    os.makedirs(temp_directory, exist_ok=True)

    # Get a list of all audio files in the source directory
    audio_files = [f for f in os.listdir(source_audio_directory) if f.endswith('.mp3')]

    # Prepend the absolute directory path to each audio file
    audio_files = [os.path.join(source_audio_directory, f) for f in audio_files]

    # Write the list of files to a temporary text file
    temp_audio_files_list = os.path.join(temp_directory, 'temp_audio_files.txt')
    with open(temp_audio_files_list, 'w') as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    print(f"combine_audio(): Combining audio files from {source_audio_directory} into {output_audio_file}")

    # Use ffmpeg to combine the audio files
    command = f'ffmpeg -f concat -safe 0 -i {temp_audio_files_list} -c copy {output_audio_file}'
    ffmpeg_output = subprocess.run(command, shell=True)

    # Clean up temporary file
    os.remove(temp_audio_files_list)

    # Check the return code of FFmpeg command
    if ffmpeg_output.returncode == 0:
        print(f"combine_audio(): Combined audio file saved as {output_audio_file}")
    else:
        print(f"combine_audio(): FFmpeg command failed with return code {ffmpeg_output.returncode}")

if __name__ == '__main__':
    # Test the function
    import read_config
    config = read_config.read_json()
    combine_audio(config)
