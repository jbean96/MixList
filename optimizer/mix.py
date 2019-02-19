import numpy
from analyzer.analyzer import song
from . import song_vector
from . import transition

class MixSequence(object):
    """
    Represents a mix between a sequence of songs in the order
    Initially two, later >= 2
    """
    def __init__(self, track_a: song.Song, track_b: song.Song):
        """
        Intializes a mix_sequence instance
        """
        self.track_a = track_a
        self.track_b = track_b
        # compute difference between the two song vectors
        vec_a = song_vector.SongVector(track_a)
        vec_b = song_vector.SongVector(track_b)
        self.diff = numpy.absolute(vec_a.get_data - vec_b.get_data)
    
    def apply_transition(self, transition: transition.Transition):
        self.diff = numpy.multiply(self.diff, transition.get_data())