import numpy, random
from enum import Enum
from typing import List, Dict
from analyzer.usersong import UserSong
from analyzer.song import Song
from analyzer.analysis import Feature
from optimizer.mix import Mix 
from optimizer.style import Style
from optimizer.threshold import Cue
from composer.audio_effect_types import Transition_Types, Effect_Types

class Lengths(Enum):
    BAR = 4
    PHRASE = 8
    HALF = 16
    VERSE = 32
    LONG = 64

class Section(object):

    def __init__(self, offset: int, length: Lengths, types: List[Transition_Types]):
        self.offset = offset
        self.length = length
        self.type = types
    
    def __str__(self):
        return str(self.to_script())
    
    def __repr__(self):
        return str(self.to_script())

    def to_script(self) -> Dict:
        return {"offset": self.offset, "length": self.length.value, "type": self.type}

class Effect(object):

    def __init__(self, offset: int, length: Lengths, types: List[Effect_Types]):
        self.offset = offset
        self.length = length
        self.type = types

    def __str__(self):
        return str(self.to_script())
    
    def __repr__(self):
        return str(self.to_script())
    
    def to_script(self) -> Dict:
        return {"offset": self.offset, "length": self.length.value, "type": self.type}

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
        list_of_sections = list()
        for section in self.sections:
            list_of_sections.append(section.to_script())
        return {"song_a": self.mix.track_a, "song_b": self.mix.track_b, "start_a": self.start_a, "start_b": self.start_b, "sections": list_of_sections}
    
    def simple(self):
        """
        Sets the state of this transition to have attributes that represent
        a 32 beat crossfade and sliding tempo change from track_a to track_b in the Mix.
        """
        track_a_len = len(self.mix.track_a.get_analysis_feature(Feature.BEATS))
        track_b_len = len(self.mix.track_b.get_analysis_feature(Feature.BEATS))
        assert track_a_len >= 32
        assert track_b_len >= 32
        # start 32 beats from the end of track_a
        self.start_a = track_a_len - 33
        # start at the beginning of track_b
        self.start_b = 0
        # construct the 32 beat crossfade and sliding tempo change section
        self.sections = [Section(offset=0, length=Lengths.VERSE, types=[Transition_Types.TEMPO_MATCH, Transition_Types.CROSSFADE])]
        self.effects = None
    
    def find_ideal_mix_points(self, length: Lengths, step_a: int, step_b: int) -> tuple:
        """
        Find the best beat to transition for this mix considering amplitude of track_a and track_b throughout the songs.
        Search sections of each song for the given length in increments at the given step.
        """
        # find optimal point in track_a to transition based on amplitude
        assert isinstance(self.mix.track_a, UserSong)
        assert isinstance(self.mix.track_b, UserSong)
        # get the beat arrays for both songs
        track_b_beats = self.mix.track_b.get_analysis_feature(Feature.BEATS)
        track_a_beats = self.mix.track_a.get_analysis_feature(Feature.BEATS)
        # calculate the number of beats
        num_beats_in_a = len(track_a_beats)
        num_beats_in_b = len(track_b_beats)
        # make sure that the transition fits in this mix
        assert num_beats_in_a >= length.value
        assert num_beats_in_b >= length.value

        # used for calculating average amplitude windows
        half_of_length = (length.value // 2)

        # make sure we're not trying to find the amplitude of a beat before/after the song, step by half_of_length
        # store all the amplitudes for steps (don't recalculate)
        b_amplitudes = list()
        for i in range(0, num_beats_in_b - length.value, step_b):
            beat_to_check_b = i + half_of_length
            track_b_curr_amp = self.mix.track_b.get_amplitude_at_beat(beat=track_b_beats[beat_to_check_b], window_size=half_of_length)
            b_amplitudes.append((i, track_b_curr_amp))
        a_amplitudes = list()
        for i in range(0, num_beats_in_a - length.value, step_a):
            beat_to_check_a = i + half_of_length 
            track_a_curr_amp = self.mix.track_a.get_amplitude_at_beat(beat=track_a_beats[beat_to_check_a], window_size=half_of_length)
            a_amplitudes.append((i, track_a_curr_amp))

        min_for_length = (None, None, 2.0) # beat and amplitude difference

        for b_amp in b_amplitudes:
            for a_amp in a_amplitudes:
                diff = abs(a_amp[1] - b_amp[1])
                if diff < min_for_length[2]:
                    min_for_length = (a_amp[0], b_amp[0], diff)

        return min_for_length
    
    def find_ideal_start_beat(self, start_b: int, length: Lengths, step: int) -> tuple:
        """
        Find the best beat to transition for this mix considering amplitude of track_a and track_b.
        Search sections of the given length for a given step.
        """
        # find optimal point in track_a to transition based on amplitude
        assert isinstance(self.mix.track_a, UserSong)
        assert isinstance(self.mix.track_b, UserSong)
        # get the beat arrays for both songs
        track_b_beats = self.mix.track_b.get_analysis_feature(Feature.BEATS)
        track_a_beats = self.mix.track_a.get_analysis_feature(Feature.BEATS)
        # calculate the number of beats
        num_beats_in_a = len(track_a_beats)
        num_beats_in_b = len(track_b_beats)
        # make sure that the transition fits in this mix
        assert num_beats_in_a >= length.value
        assert num_beats_in_b >= length.value
        # make sure that the start_b is within b
        assert (start_b + length.value) < num_beats_in_b and start_b < num_beats_in_b
        half_of_length = (length.value // 2)
        track_b_start_amp = self.mix.track_b.get_amplitude_at_beat(beat=track_b_beats[start_b + half_of_length], window_size=half_of_length)
        min_for_length = (None, 2.0) # beat and amplitude difference
        # make sure we're not trying to find the amplitude of a beat before/after the song, step by half_of_length
        for i in range(0, num_beats_in_a - length.value, step):
            beat_to_check = i + half_of_length 
            track_a_curr_amp = self.mix.track_a.get_amplitude_at_beat(beat=track_a_beats[beat_to_check], window_size=half_of_length)
            diff = abs(track_a_curr_amp - track_b_start_amp)
            if diff < min_for_length[1]:
                min_for_length = (i, diff)
        
        return min_for_length

        # consider starting point in track_a

        # create tempo match section

        # create fade section

        # merge the sections if necessary
    
    def create_random_transition(self):
        """
        Sets the state of this transition to be a randomnly selected length, type and
        location in track_a and track_b of the Mix.
        """
        # set start_b to 0
        self.start_b = 0
        # choose length
        length = random.sample([Lengths.BAR, Lengths.PHRASE, Lengths.HALF, Lengths.VERSE], 1)[0]
        # choose start into track a
        track_a_beats = self.mix.track_a.get_analysis_feature(Feature.BEATS)
        number_of_verses = len(track_a_beats) // Lengths.VERSE.value
        # somewhere after the first verse and before the last verse
        assert len(track_a_beats) >= length.value
        # select a start point at anywhere between first verse and last full verse
        self.start_a = (random.randint(1, number_of_verses - 1)) * (Lengths.VERSE.value)
        # build the section based on length:
        types = None
        if length == Lengths.BAR: 
            # just a crossfade
            types = [Transition_Types.CROSSFADE]
        elif length == Lengths.PHRASE or Lengths.HALF:
            # crossfade with tempo match continious
            types=[Transition_Types.CROSSFADE, Transition_Types.TEMPO_MATCH]
        else:
            # crossfade with tempo match half way
            types=[Transition_Types.CROSSFADE, Transition_Types.TEMPO_MATCH2]
        self.sections = [Section(offset=0, length=length, types=types)]
    
    def create_last_track_outro(self):
        """
        Creates a smooth fade out for the last track of a mix.
        """
        raise NotImplementedError()
    
    def create_ideal_intro_transition(self):
        """
        Sets the state of this transition to be an ideal one based on various heuristics.
        """
        # find the optimal minimum length for the given tempo change
        tempo_change = abs(self.mix.threshold[Cue.TEMPO.value])

        length = None
        # pick a transition length based on tempo change
        # if the tempo change is within a standard of the DJ's style
        if tempo_change <= self.style.dev[Cue.TEMPO.value]:
            # reasonable lengths
            length = random.sample([Lengths.HALF, Lengths.VERSE], 1)[0]
        else:
            # go short or gooo long
            length = random.sample([Lengths.BAR, Lengths.PHRASE, Lengths.LONG], 1)[0]

        # if the songs have similar valence then use something in the middle
        self.start_b = 0
        self.start_a = self.find_ideal_start_beat(self.start_b, length, length.value // 2)[0]

        # build the section based on length:
        types = None
        if length == Lengths.BAR: 
            # just a crossfade
            types = [Transition_Types.CROSSFADE]
        elif length == Lengths.PHRASE or length == Lengths.HALF:
            # crossfade with tempo match continious
            types=[Transition_Types.CROSSFADE, Transition_Types.TEMPO_MATCH]
        else:
            # crossfade with tempo match 
            types=[Transition_Types.CROSSFADE, 
                   random.sample([Transition_Types.TEMPO_MATCH, 
                                  Transition_Types.TEMPO_MATCH2], 1)[0]]

        self.sections = [Section(offset=0, length=length, types=types)]
    
    # TODO: step 1 find ideal length, based on song amplitude at a given point (add ability to detect vocals later)
    # TODO: find ideal location to transition (amplitude, progress, bonus points for correct phrasing)
    # TODO: apply echo if the transition needs it on the way out
    # TODO: add a "to script" method which converts the transition to a valid script for composer