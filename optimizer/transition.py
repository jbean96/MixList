import numpy
from enum import Enum
from .mix import Mix 
from .style import Style
from analyzer.usersong import UserSong
from analyzer.song import Song
from analyzer.analysis import Feature
from typing import List, Dict
from composer.audio_effect_types import Transition_Types, Effect_Types

class Transition(object):
    """
    Represents a "transition" between two songs.
    Creates an ideal transition between two songs given a Mix and a Style.
    """

    def __init__(self, mix: Mix, style: Style):
        """
        Creates a new transition object.
        """
        self.mix = mix
        self.style = style
        self.start_a = None
        self.start_b = None
        self.sections = None # later list() of sections
        self.effects = None # later list() of effects
    
    def to_script(self) -> Dict:
        return {"song_a": self.mix.track_a, "song_b": self.mix.track_b, "start_a": self.start_a, "start_b": self.start_b, "sections": self.sections}
    
    def simple_LONG(self):
        """
        Sets the state of this transition to have attributes that represent
        a 32 beat crossfade and sliding tempo change from track_a to track_b in the Mix.
        """
        track_a_len = len(self.mix.track_a.get_analysis_feature(Feature.BEATS))
        track_b_len = len(self.mix.track_b.get_analysis_feature(Feature.BEATS))
        assert track_a_len >= 32
        assert track_b_len >= 32
        # start 32 beats from the end of track_a
        self.start_a = track_b_len - 33
        # start at the beginning of track_b
        self.start_b = 0
        # construct the 32 beat crossfade and sliding tempo change section
        self.sections = [Section(offset=0, length=Lengths.VERSE, types=[Transition_Types.TEMPO_MATCH, Transition_Types.CROSSFADE])]
        self.effects = None
    
    @staticmethod
    def find_ideal_start_beat(mix: Mix) -> List[tuple]:
        """
        Find the best beat to transition for this mix considering amplitude of track_a and track_b.
        """
        # consider starting section of track_b
        # all the generated mixes
        # TODO: assert that a song is a UserSong
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

class Section(object):

    def __init__(self, offset: int, length: Lengths, types: List[Transition_Types]):
        self.offset = offset
        self.length = length
        self.type = types

    def to_script(self) -> Dict:
        return {"offset": self.offset, "length": self.length.value, "type": self.type}

class Effect(object):

    def __init__(self, offset: int, length: Lengths, types: List[Effect_Types]):
        self.offset = offset
        self.length = length
        self.type = types
    
    def to_script(self) -> Dict:
        return {"offset": self.offset, "length": self.length.value, "type": self.type}

class Lengths(Enum):
    BAR = 4
    PHRASE = 8
    HALF = 16
    VERSE = 32
    LONG = 64