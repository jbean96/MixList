# pylint: disable=import-error
# pylint: disable=no-name-in-module

import sys

sys.path.append("..")

from analyzer import analysis

beats = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
beats = list(map(analysis.Beat, beats))

def test_no_downbeats():
    for beat in beats:
        assert beat.is_downbeat == False

def test_three_time_signature():
    threes = analysis.annotate_downbeats(beats, 3)
    for (i, beat) in enumerate(threes):
        if i % 3 == 0:
            assert beat.is_downbeat == True
        else:
            assert beat.is_downbeat == False

def test_four_time_signature():
    fours = analysis.annotate_downbeats(beats, 4)
    for (i, beat) in enumerate(fours):
        if i % 4 == 0:
            assert beat.is_downbeat == True
        else:
            assert beat.is_downbeat == False