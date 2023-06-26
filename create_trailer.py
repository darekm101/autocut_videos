import os
import read_configs
import get_beats
import get_audio_meta
import match_source_video
import cut_video_clips
import combine_clips
import trim_audio

configs = read_configs.read_environment()
print(f"Read configs: {configs}")
get_audio_meta.get_audio_meta(configs)
match_source_video.generate_video_cuts(configs)
cut_video_clips.cut_video_clips(configs)
trim_audio.trim_audio(configs)
combine_clips.combine_clips(configs)
