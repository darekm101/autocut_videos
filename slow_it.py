import os
import sys
import glob
import subprocess

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith('.mp4'):
            input_file = os.path.join(root, file)
            print(f"Processing input file: {input_file}")

            base_file_name = os.path.basename(input_file).split(".")[0]
            relative_path = os.path.relpath(root, input_dir)
            output_sub_dir = os.path.join(output_dir, relative_path)

            if not os.path.exists(output_sub_dir):
                os.makedirs(output_sub_dir)
                print(f"Created output subdirectory: {output_sub_dir}")

            output_file = os.path.join(output_sub_dir, f"{base_file_name}_output.mp4")
            print(f"Set output file path to: {output_file}")

            raw_file = os.path.join(output_sub_dir, f"{base_file_name}_raw.h265")

            try:
                command = [
                    'ffmpeg', '-i', input_file, 
                    '-map', '0:0', '-c:v', 'copy', '-bsf:v', 'hevc_mp4toannexb', 
                    raw_file
                ]
                subprocess.run(command, check=True)
                print("Converted video to raw bitstream format")

                command = [
                    'ffmpeg', '-fflags', '+genpts', '-r', '30', 
                    '-i', raw_file, '-c:v', 'copy', '-tag:v', 'hvc1',
                    output_file
                ]
                subprocess.run(command, check=True)
                print("Generated new timestamps and muxed to container")

                os.remove(raw_file)
                print("Deleted raw file")
            except subprocess.CalledProcessError as e:
                print(f"Error processing file {input_file}: {e}")
                continue

print("Video processing completed.")
