import os
import subprocess

def add_audio_to_video(config):
    print(f"________ MODULE: combine_media.py ___________")

    output_directory = config['output_directory']
    final_movie_title = config['final_movie_title']

    video_file = os.path.join(output_directory, f"{final_movie_title}.mp4")
    print(f"video_file: {video_file}")
    audio_file = os.path.join(output_directory, f"{final_movie_title}_trimmed.mp3")
    print(f"audio_file: {audio_file}")

    output_file = os.path.join(output_directory, f"{final_movie_title}_final.mp4")
    print(f"output_file: {output_file}")

    # Use ffmpeg to combine the audio and video files
    command = f"ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental {output_file}"
    ffmpeg_output = subprocess.run(command, shell=True)

    # Check the return code of FFmpeg command
    if ffmpeg_output.returncode == 0:
        print(f"add_audio_to_video(): Final movie with audio saved as {output_file}")
    else:
        print(f"add_audio_to_video(): FFmpeg command failed with return code {ffmpeg_output.returncode}")

if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    add_audio_to_video(config)

