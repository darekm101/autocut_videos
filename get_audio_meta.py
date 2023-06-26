from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np
import json
import os

def get_audio_meta(config): 

    directory = config["source_audio_files"]
    files = os.listdir(directory)

    file = next((f for f in files if f.endswith(('.mp3', '.wav'))), None)

    if file is None:
        print(f"No mp3 or wav files found in the directory {directory}.")
        exit()

    file_path = os.path.join(directory, file)

    output_directory = config["temp_audio_configs"]
    os.makedirs(output_directory, exist_ok=True)

    json_path = os.path.join(output_directory, f'{file.split(".")[0]}.json')

    # check if the output JSON file already exists
    if os.path.isfile(json_path):
        print(f"Output JSON file {json_path} already exists. Skipping processing for file {file}...")
        return

    if file.endswith('.mp3'):
        print("Converting mp3 to wav...")
        audio = AudioSegment.from_mp3(file_path)
        audio.export("file.wav", format="wav")
        file_path = "file.wav"

    print(f"Reading audio file: {file_path}...")
    sample_rate, data = wavfile.read(file_path)

    duration = len(data) / sample_rate
    print(f"Audio duration: {duration} seconds")

    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    bin_size = 0.1
    points_per_bin = int(sample_rate * bin_size)

    print(f"Calculating moving average with bin size: {bin_size} seconds and points per bin: {points_per_bin}...")
    moving_avg = np.convolve(data, np.ones(points_per_bin) / points_per_bin, mode='same')
    moving_stddev = np.array([np.std(data[max(0,i-points_per_bin//2):i+points_per_bin//2]) for i in range(len(data))])

    print("Finding spikes...")
    threshold = 3
    cooldown = int(sample_rate)  # cooldown of 1 second
    last_spike = -cooldown
    spikes = []
    for i in range(len(data)):
        if data[i] > moving_avg[i] + threshold * moving_stddev[i] and i > last_spike + cooldown:
            spikes.append(i)
            last_spike = i

    spikes_seconds = list(np.array(spikes) / sample_rate)

    json_data = [{"sequence_number": i,
            "duration_from_last": spikes_seconds[i+1] - spikes_seconds[i] if i+1 < len(spikes_seconds) else spikes_seconds[i+1],
            "duration_from_start": spikes_seconds[i+1],
            "video_cut_point": True,
            "video_sequence_id": i} for i in range(1, len(spikes_seconds)-1)]

    print("Writing output to JSON file...")
    with open(json_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

    print("Finished.")

if __name__ == "__main__":

    import read_configs
    config = read_configs.read_environment()
    
    get_audio_meta(config)