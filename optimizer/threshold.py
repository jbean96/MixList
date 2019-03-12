import numpy
from .mix import Comp

class Threshold(object):
    """
    Represents a "threshold" to evaluate a mix, common states represent
    a DJ's style threshold or goal progress threshold.
    Can represent either a min, max, "ideal" state (no range)

    For example, using features: [TEMPO, KEY, DANCEABILITY, ENERGY, VALENCE]
    """

    def __init__(self, values: numpy.array):
        """
        Initializes a threshold instance
        """
        assert numpy.size(values) == len(Comp)
        self.data = values
    
    def get_data(self) -> numpy.array:
        """
        Returns the data for this Threshold object
        """
        return self.data