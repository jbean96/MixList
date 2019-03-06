
import os
import json
import pickle
import sys
import fnmatch

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

song_paths = get_file_paths(os.path.join(os.getcwd(), "djskinnyg_songs"))
print(song_paths)
song_objects = list() 

for path in song_paths:
    song = usersong.UserSong(path, True)
    song_objects.append(song)
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
dj = optimizer.Optimizer(song_objects, None, None, goals)
print(dj.generate_mixtape())
