# pylint: disable=import-error
# pylint: disable=no-name-in-module

import os
import sys
import json

sys.path.append("..")

from analyzer import analysis
from analyzer import util

def test_no_downbeats():
    beats = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    beats = list(map(analysis.Beat, beats))
    for beat in beats:
        assert beat.is_downbeat == False

def test_three_time_signature():
    beats = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    beats = list(map(analysis.Beat, beats))
    threes = analysis.annotate_downbeats(beats, 3)
    for (i, beat) in enumerate(threes):
        if i % 3 == 0:
            assert beat.is_downbeat == True
        else:
            assert beat.is_downbeat == False

def test_four_time_signature():
    beats = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    beats = list(map(analysis.Beat, beats))
    fours = analysis.annotate_downbeats(beats, 4)
    for (i, beat) in enumerate(fours):
        if i % 4 == 0:
            assert beat.is_downbeat == True
        else:
            assert beat.is_downbeat == False

def test_find_closest_beat():
    beats = list(map(analysis.Beat, [i * (util.SAMPLE_RATE if analysis.Beat.INDEX_VALUE == 'samples' else 1.0) for i in range(21)]))
    beats = analysis.annotate_downbeats(beats, util.DEFAULT_TIME_SIGNATURE)
    assert analysis.get_closest_beat_to_time(beats, 1.51, False) == beats[2]
    assert analysis.get_closest_beat_to_time(beats, 2.78, False) == beats[3]
    assert analysis.get_closest_beat_to_time(beats, 2.49, False) == beats[2]
    assert analysis.get_closest_beat_to_time(beats, 13.01, False) == beats[13]

def test_find_closest_downbeat():
    beats = list(map(analysis.Beat, [i * (util.SAMPLE_RATE if analysis.Beat.INDEX_VALUE == 'samples' else 1.0) for i in range(21)]))
    beats = analysis.annotate_downbeats(beats, util.DEFAULT_TIME_SIGNATURE)
    assert analysis.get_closest_beat_to_time(beats, 1.51, True) == beats[0]
    assert analysis.get_closest_beat_to_time(beats, 2.78, True) == beats[4]
    assert analysis.get_closest_beat_to_time(beats, 2.49, True) == beats[4]
    assert analysis.get_closest_beat_to_time(beats, 13.01, True) == beats[12]
    assert analysis.get_closest_beat_to_time(beats, 17.99, True) == beats[16]
    assert analysis.get_closest_beat_to_time(beats, 18.01, True) == beats[20]

def test_load_analysis_from_file():
    mapping_path = os.path.join(os.curdir, "files", "mapping.json")
    with open(mapping_path, "r") as mapping_in:
        mapping = json.loads(mapping_in.read())
        mapping_in.close()
    for key in mapping:
        analysis_path = os.path.join(os.curdir, "files", "analyses", key)
        loaded_analysis = analysis.from_file(analysis_path)
        assert type(loaded_analysis) == analysis.Analysis
        assert loaded_analysis.is_analyzed(analysis.Feature.NAME) == True
        assert loaded_analysis.is_analyzed(analysis.Feature.BEATS) == True
        assert loaded_analysis.is_analyzed(analysis.Feature.TEMPO) == True
        assert loaded_analysis.is_analyzed(analysis.Feature.DURATION) == True
        assert loaded_analysis.is_analyzed(analysis.Feature.VALENCE) == False