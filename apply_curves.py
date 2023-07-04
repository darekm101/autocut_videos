import os
import subprocess
import json

def apply_curves(config):
    print(f"________ MODULE: apply_curves.py ___________")

    # Retrieve configuration values
    output_directory = config['output_directory']
    final_movie_title = config['final_movie_title']

    # Path of the final video file
    final_video_path = os.path.join(output_directory, f"{final_movie_title}.mp4")

    # Apply curves to the final video
    output_video = os.path.join(output_directory, f"{final_movie_title}_curved.mp4")

    # FFmpeg command to apply curves to the video
    command = f"ffmpeg -i {final_video_path} -vf \"curves=all='0/0 0.25/0.15 1/1',format=yuv420p\" -c:v libx264 -crf 18 -preset ultrafast {output_video}"


    ffmpeg_output = subprocess.run(command, shell=True)

    # Check the return code of FFmpeg command
    if ffmpeg_output.returncode == 0:
        print(f"apply_curves(): Curves applied to {final_video_path}. Output saved as {output_video}")
    else:
        print(f"apply_curves(): Failed to apply curves to {final_video_path}.")

if __name__ == '__main__':
    import read_config
    config = read_config.read_json()
    apply_curves(config)
