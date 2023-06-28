import os
import subprocess
import json

def synch_audio_video(config):
    print(f"________ MODULE: match_media_duration.py ___________")

    temp_directory = os.path.abspath(config['temp_directory'])
    print(f"temp_directory: {temp_directory}")
    output_directory = config['output_directory']
    print(f"output_directory: {output_directory}")
    final_movie_title = config['final_movie_title']
    print(f"final_movie_title: {final_movie_title}")

    audio_file = os.path.join(temp_directory, f"{final_movie_title}.mp3")
    print(f"audio_file: {audio_file}")
    video_file = os.path.join(output_directory, f"{final_movie_title}.mp4")
    print(f"video_file: {video_file}")

    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file]
    video_duration = float(subprocess.check_output(command).decode('utf-8').strip())
    print(f"video_duration: {video_duration}")

    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_file]
    audio_duration = float(subprocess.check_output(command).decode('utf-8').strip())
    print(f"audio_duration: {audio_duration}")

    if audio_duration > video_duration:
        print(f"Audio duration is longer than video duration. Trimming audio.")
        trimmed_audio_file = os.path.join(output_directory, f"{final_movie_title}_trimmed.mp3")
        print(f"trimmed_audio_file: {trimmed_audio_file}")
        command = ['ffmpeg', '-y', '-i', audio_file, '-t', str(video_duration), '-c', 'copy', trimmed_audio_file]
        print(f"command: {command}")
        ffmpeg_output = subprocess.run(command, check=True)
        print(f"ffmpeg_output: {ffmpeg_output}")
        if ffmpeg_output.returncode == 0:
            print(f"Trimmed audio file saved as {trimmed_audio_file}")
        else:
            print(f"FFmpeg command failed with return code {ffmpeg_output.returncode}")
    else:
        print(f"Audio duration is shorter or equal to video duration. No trimming required.")

if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    print(f"config: {config}")
    synch_audio_video(config)
