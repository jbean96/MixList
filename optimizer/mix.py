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
        Intializes a mix_sequence instance
        """
        self.track_a = track_a
        self.track_b = track_b
        # compute difference between the two song vectors
        self.diff = numpy.array([1,1,1,1])
    
    def apply_transition(self, transition: transition.Transition):
        self.diff = numpy.multiply(self.diff, transition.get_data())


    # mix: [1, 2, 3, 4]
    # transition: [(1 + 2 + 3), (1 + 2 + 3), ...]
    # mix: [i, j, k, l]
    # transition [i + j + k, i * 2 + j, ...]


    # consider comparing each feature on a song to song basis