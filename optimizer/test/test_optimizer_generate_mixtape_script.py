
import os
import json
import pickle
import sys
import fnmatch
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..")))
print(sys.path)
from analyzer.analyzer import usersong
from analyzer.analyzer import analysis
from optimizer import optimizer
from optimizer import mix_goal
from optimizer import style
from optimizer import threshold

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

# song_paths = get_file_paths(os.path.join(os.getcwd(), "djskinnyg_songs"))
song_paths = get_file_paths(os.path.join("..", "..", "testmp3s", "songs", "other"))
song_objects = usersong.batch_create_user_songs(song_paths)
usersong.batch_analyze_user_songs(song_objects)

for song in song_objects:
    print("{} : {} : {}".format(song.get_analysis_feature(analysis.Feature.NAME), song.get_analysis_feature(analysis.Feature.TEMPO), song.get_analysis_feature(analysis.Feature.KEY)))

# style threshold design
"""
min_t = threshold.threshold
max_t = threshold.Threshold
style = style.Style() 
"""
# create a list with one goal (start)
first_goal = mix_goal.MixGoal(song_objects[0], 0.0)
goals = list([first_goal])
# initialize optimizer
dj = optimizer.Optimizer(song_objects, goals, None, None)
mix_script = dj.generate_mixtape()
print("***MIX SCRIPT RESULT***")

print(mix_script)
