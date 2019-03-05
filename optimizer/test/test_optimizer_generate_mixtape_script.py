
import os
import json
import pickle
import sys

sys.path.append("../..")

from analyzer.analyzer import analysis
from analyzer.analyzer import song
from analyzer.analyzer import matcher
from analyzer.analyzer import spotify
from optimizer import mix_goal
from optimizer import optimizer

SPOTIFY_PREFIX = "spotify:track:"

mapping_path = os.path.join(os.curdir, "..", "..", "analyzer", "test", "files", "mapping.json")
with open(mapping_path, "r") as mapping_in:
    mapping = json.loads(mapping_in.read())
    mapping_in.close()

song_objects = list()
for key in mapping:
    analysis_path = os.path.join(os.curdir, "files", "analyses", key)
    loaded_analysis = analysis.from_file(analysis_path)
    s = song.Song(loaded_analysis.get_feature(analysis.Feature.NAME))
    s.set_analysis(loaded_analysis)
    sp_song = matcher.match_song(s)
    song_objects.append(s)

# create a list with one goal (start)
first_goal = mix_goal.MixGoal(song_objects[0], 0.0)
goals = list([first_goal])

# initialize optimizer
dj = optimizer.Optimizer(song_objects, None, None, goals)

print(dj.generate_mixtape)
