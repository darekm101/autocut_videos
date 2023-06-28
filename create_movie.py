import os
import read_config
import combine_audio
import make_initial_cutlist
import match_clips_to_cuts
import make_video_json


config = read_config.read_json()
combine_audio.combine_audio(config)
make_initial_cutlist.write_json(config)
make_video_json.write_json(config)





# print(f"Read configs: {configs}")
# get_audio_meta.get_audio_meta(configs)
# match_source_video.generate_video_cuts(configs)
# cut_video_clips.cut_video_clips(configs)
# trim_audio.trim_audio(configs)
# combine_clips.combine_clips(configs)
