import json
import os

def write_json(config):
    print(f"________ MODULE: make_video_json.py ___________")

    initial_cut_list_file = config['initial_cutlist']
    output_file = os.path.join(config['temp_directory'], 'movie.json')

    with open(initial_cut_list_file, 'r') as f:
        initial_cut_list = json.load(f)

    cut_list_video_true = [i for i in initial_cut_list if i['video_cut_point']]

    for cut_point in cut_list_video_true:
        cut_point["clip_duration"] = cut_point.pop("duration_from_last_video_cut_point")
        cut_point.pop("sequence_number")
        cut_point.pop("video_cut_point")
        cut_point.pop("duration_from_last")
        
    cut_list_video_true_sorted = sorted(cut_list_video_true, key=lambda k: k['video_sequence_id'])
    
    # Making 'video_sequence_id' the top item in each dictionary
    for item in cut_list_video_true_sorted:
        item = {k: item[k] for k in sorted(item.keys(), reverse=True)}

    with open(output_file, 'w') as json_file:
        json.dump(cut_list_video_true_sorted, json_file, indent=4)

    print(f"write_json(): Video cut list written to {output_file}")


if __name__ == '__main__':
    # Test the function
    import read_config
    config = read_config.read_json()
    write_json(config)
