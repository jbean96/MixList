import numpy
from analyzer.analyzer.song import Song
from analyzer.analyzer.analysis import Feature
from . import transition

class Mix(object):
    """
    Represents a mix between a sequence of songs in the order
    Initially two, later >= 2

    Later version features:
        - consider different sections of each song
        - consider multiple songs
    """
    def __init__(self, track_a: Song, track_b: Song):
        """
        Keyword Args:
            track_a: a Song instance representing the starting song in this mix.
            track_b: a Song instance representing the end song in this mix.
        
        Initializes a new Mix instance with no transition history, compares the start
        and end song without factoring in a transition.
        """
        self.track_a = track_a
        self.track_b = track_b
        # a history of transitions applied to this Mix, 0 index is the least recent.
        self.tran_history = numpy.array([]) 
        # compute difference between the two song vectors
        self.comp_vector = numpy.array([1,1,1,1])
    
    @classmethod
    def from_old_mix(self, old_mix: 'Mix', transition: transition.Transition, new_comp: numpy.array):
        """
        Keyword Args:
            old_mix: a Mix instance to copy.
            transition: a transition to add to the new Mix instances transition history.
            new_comp: the comparison vector to use for the new Mix instance.
        
        Initializes a new Mix instance as a copy of the old_mix instance with transition
        added to the end of its transition history.
        """
        self.track_a = old_mix.track_a
        self.track_b = old_mix.track_b
        old_trans = list()
        for t in old_mix.tran_history:
            old_trans.append(t)
        old_trans.append(transition)
        self.tran_history = numpy.array(old_trans)
        self.comp_vector = new_comp

    def apply_transition(self, tran: transition.Transition) -> 'Mix':
        """
        Keyword Args:
            tran: a Transition instance to be applied to this Mix object.

        Takes a transition and returns a new Mix object representing
        the mix between two songs using the given Transition, the new Mix object
        has the transition recorded in its history.
        """
        # apply the transition to the two songs "comparison"
        new_comp_vector = numpy.multiply(self.comp_vector, tran.get_data())
        # return a new Mix instance with updated transition history and comparison
        return self.from_old_mix(old_mix=self, transition=tran, new_comp=new_comp_vector)

    def __compare_songs(self, track_a: Song, track_b: Song) -> numpy.array:
        """
        Returns a numpy array that represents the comparison vector between track_a
        into track_b in the form:
        [TEMPO_DIFF, KEY_DIFF, DANCEABILITY_DIFF, ENERGY_DIFF, VALENCE_DIFF]
        If any feature for either Song in a comparison is not analyzed that index will be NaN
        """
        # compare tempo
        tempo_diff = track_b.get_analysis_feature(Feature.TEMPO) - track_a.get_analysis_feature(Feature.TEMPO)
        # compare key
        # get the distance between keys according to the Camelot wheel.
        key_diff = numpy.nan
        # compare danceability
        dance_diff = track_b.get_analysis_feature(Feature.DANCEABILITY) - track_a.get_analysis_feature(Feature.DANCEABILITY)
        # compare energy
        energy_diff = track_b.get_analysis_feature(Feature.ENERGY) - track_a.get_analysis_feature(Feature.ENERGY) 
        # compare valence
        val_diff = track_b.get_analysis_feature(Feature.VALENCE) - track_a.get_analysis_feature(Feature.VALENCE)
        # return comparison vector
        return numpy.array([tempo_diff, key_diff, dance_diff, energy_diff, val_diff])