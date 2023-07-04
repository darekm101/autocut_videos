import os
import read_config
import combine_audio
import make_initial_cutlist
import make_video_json
import match_clips_to_cuts
import cut_video_clips
import apply_curves
import render_movie
import match_media_duration
import combine_media


config = read_config.read_json()
combine_audio.combine_audio(config)
make_initial_cutlist.write_json(config)
make_video_json.write_json(config)
match_clips_to_cuts.assign_clips(config)
cut_video_clips.cut_video_clips(config)
render_movie.combine_all(config)
if config['apply_curves']:
    apply_curves.apply_curves(config)
if config['add_logo']: 
    apply_logo.run(config)
match_media_duration.synch_audio_video(config)
combine_media.add_audio_to_video(config)

