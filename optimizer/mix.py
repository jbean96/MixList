import numpy
from analyzer.analyzer import song
from . import transition

class Mix(object):
    """
    Represents a mix between a sequence of songs in the order
    Initially two, later >= 2

    Later version features:
        - consider different sections of each song
        - consider multiple songs
    """
    def __init__(self, track_a: song.Song, track_b: song.Song):
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
    
    def __init__(self, old_mix: Mix, transition: transition.Transition, new_comp: numpy.array):
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

    def apply_transition(self, transition: transition.Transition) -> Mix:
        """
        Keyword Args:
            transition: a Transition instance to be applied to this Mix object.

        Takes a transition and returns a new Mix object representing
        the mix between two songs using the given Transition, the new Mix object
        has the transition recorded in its history.
        """
        # apply the transition to the two songs "comparison"
        # return a new Mix instance with updated transition history and comparison


    def __compare_songs(self) -> numpy.array:
        """
        Returns a numpy array that represents the comparison vector between track_a
        into track_b for this mix.
        """
        return None

    # mix: [1, 2, 3, 4]
    # transition: [(1 + 2 + 3), (1 + 2 + 3), ...]
    # mix: [i, j, k, l]
    # transition [i + j + k, i * 2 + j, ...]


    # consider comparing each feature on a song to song basis