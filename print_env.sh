echo "Let's write a movie editing python script with ffmpeg which will edit movie clips to music and combine them."=
echo "Always follow these rules." 
echo "After this initial post, just say Got it! and nothing else, wait for more instructions."
echo " Don't include code comment in new code, instead use print statements with parameters and values"
echo " Don't use moviepy library, instead always use ffmpeg with subprocess"
echo "Always try to break up the code into small functions, avoid writing long functions"
echo "The main script is called create_movie.py and here are the contents"
cat create_movie.py
echo "The configuration file config.json is as follows"
cat config.json
echo "The script that reads the configuration file is called read_config.py and here are the contents"
cat read_config.py 
echo "Next is combine_audio.py, here are the contents"
cat combine_audio.py
echo "Next is make_initial_cutlist.py, here are the contents"
cat make_initial_cutlist.py
echo "Next is make_movie_json.py, here are the contents"
cat make_movie_json.py
echo "Next is match_clips_to_cuts.py, here are the contents"
cat match_clips_to_cuts.py
echo "Next is cut_video_clips.py, here are the contents"
cat cut_video_clips.py

















