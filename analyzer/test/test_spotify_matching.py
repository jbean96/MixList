# pylint: disable=no-name-in-module

import os
import json
import pickle
import sys

sys.path.append("..")

from analyzer import analysis
from analyzer import song
from analyzer import matcher
from analyzer import spotify

SPOTIFY_PREFIX = "spotify:track:"

def test_matches():
    mapping_path = os.path.join(os.curdir, "files", "mapping.json")
    with open(mapping_path, "r") as mapping_in:
        mapping = json.loads(mapping_in.read())
        mapping_in.close()
    scores = {
        "correct" : 0,
        "not_found" : 0,
        "incorrect" : 0
    }
    for key in mapping:
        analysis_path = os.path.join(os.curdir, "files", "analyses", key)
        loaded_analysis = analysis.from_file(analysis_path)
        s = song.Song(loaded_analysis.get_feature(analysis.Feature.NAME))
        s.set_analysis(loaded_analysis)
        sp_song = matcher.match_song(s)
        s
        if sp_song is None:
            scores["not_found"] += 1
        else:
            spotify_uri = SPOTIFY_PREFIX + sp_song[0].get_id()
            if spotify_uri in mapping[key]:
                scores["correct"] += 1
            else:
                scores["incorrect"] += 1
    
    print(scores)