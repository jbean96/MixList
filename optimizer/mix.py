from . import song_vector

class MixSequence(object):
    """
    Represents a mix between a sequence of songs in the order
    Initially two, later >= 2
    """
    def __init__(self, track_a, track_b):
        """
        Intializes a mix_sequence instance
        """
        # compare the songs here
        assert isinstance(track_a, song_vector.SongVector)
        assert isinstance(track_b, song_vector.SongVector)

    
    
    def apply_transition(self, transition):
        NotImplementedError()