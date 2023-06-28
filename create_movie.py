import os
import read_config
import combine_audio as combine_audio


config = read_config.read_json()
combine_audio.combine_audio(config)





# print(f"Read configs: {configs}")
# get_audio_meta.get_audio_meta(configs)
# match_source_video.generate_video_cuts(configs)
# cut_video_clips.cut_video_clips(configs)
# trim_audio.trim_audio(configs)
# combine_clips.combine_clips(configs)
