import numpy
from enum import Enum
from .mix import Mix 
from .style import Style
from analyzer.usersong import UserSong
from analyzer.song import Song
from analyzer.analysis import Feature
from typing import List

class Transition(object):
    """
    Represents a "transition" between two songs.
    Creates an ideal transition between two songs given a Mix and a Style.
    """

    # TODO: define basic transitions as class constants
        # crossfade
        # tempo change

    def __init__(self, mix: Mix, style: Style):
        """
        Creates a new transition object.
        """
        self.mix = mix
        self.style = style
        self.sections = list()
    
    def get_data(self) -> numpy.array:
        """
        Returns the data for this Transition object.
        """
        return self.data
    
    @staticmethod
    def find_ideal_start_beat(mix: Mix) -> List[tuple]:
        """
        Find the best beat to transition for this mix considering amplitude of track_a and track_b.
        """
        # consider starting section of track_b
        # all the generated mixes
        best_beats = list() 
        track_b = mix.track_b
        assert isinstance(track_b, UserSong)
        track_a = mix.track_a
        assert isinstance(track_a, UserSong)
        for length in Lengths:
            min_for_length = (None, 2.0) # beat and amplitude difference
            track_b_start_amp = track_b.get_amplitude_at_beat(beat=track_b.get_analysis_feature(Feature.BEATS[length/2]), window_size=length)
            # find the ideal matching segment in track_a
            track_a_beats = track_a.get_analysis_feature(Feature.BEATS)
            num_beats = len(track_a_beats)
            for i in range(0, num_beats):
                # make sure we're not trying to find the amplitude of a beat before/after the song
                if i >= length/2 and (i + length/2) <= num_beats:
                   track_a_curr_amp = track_a.get_amplitude_at_beat(beat=track_a_beats[i], window_size=length)
                   diff = abs(track_a_curr_amp - track_b_start_amp)
                   if diff < min_for_length[1]:
                       min_for_length = (i, diff)
            best_beats.append((length, min_for_length[0])) 

        # consider starting point in track_a

        # create tempo match section

        # create fade section

        # merge the sections if necessary

        return best_beats
    
    # TODO: step 1 find ideal length, based on song amplitude at a given point (add ability to detect vocals later)
    # TODO: find ideal location to transition (amplitude, progress, bonus points for correct phrasing)
    # TODO: apply echo if the transition needs it on the way out
    # TODO: add a "to script" method which converts the transition to a valid script for composer

class Lengths(Enum):
    QUICK = 4
    SHORT = 8
    AVERAGE = 16
    LONG = 32