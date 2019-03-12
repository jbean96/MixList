
import os
import json
import pickle
import sys
import fnmatch
project_path = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(project_path)
from analyzer import usersong
from analyzer import analysis
from optimizer import optimizer
from optimizer import mix_goal
from optimizer import style
from optimizer import threshold
from composer import composer

# TODO: @analyzer, recognize and handle version names: "(Dirty)", "(Clean)", "(Intro - Clean)", "(Intro - Dirty)", "(Remix)" using regular expressions.

def get_file_paths(directory: str):
    if not os.path.isdir(directory):
        raise Exception("%s is not a directory" % directory)
    
    file_paths = []
    for root, _, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(os.path.abspath(root), f)
            for ext in usersong.UserSong.EXTENSIONS:
                if fnmatch.fnmatch(file_path, "*%s" % ext):
                    file_paths.append(file_path)
                    break
    return file_paths

song_folder_path = os.path.normpath(os.path.join(project_path, "djskinnyg_songs"))
song_paths = get_file_paths(song_folder_path)
cache_path = os.path.normpath(os.path.join(song_folder_path, "cache"))
song_objects = usersong.batch_create_user_songs(song_paths)
usersong.batch_analyze_user_songs(song_objects, cache_path)

for song in song_objects:
    song.write_analysis_to_folder(cache_path)
    print("{} : {} : {} : {} : {} : {}".format(song.get_analysis_feature(analysis.Feature.NAME), song.get_analysis_feature(analysis.Feature.TEMPO), song.get_analysis_feature(analysis.Feature.KEY), song.get_analysis_feature(analysis.Feature.DANCEABILITY), song.get_analysis_feature(analysis.Feature.ENERGY), song.get_analysis_feature(analysis.Feature.VALENCE)))

# create a list with one goal (start)
first_goal = mix_goal.MixGoal(song_objects[0], 0.0)
goals = list([first_goal])
# initialize optimizer
dj = optimizer.Optimizer(song_objects, goals, None, style.Style_Lib.tempo_based.value)
mix_script = dj.generate_mixtape()
print("***MIX SCRIPT RESULT***")

for mix in mix_script:
    print(mix)

#c = composer.composer_parser(mix_script)

#c.compose()
