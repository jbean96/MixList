import numpy
class Threshold(object):
    """
    Represents a "threshold" to evaluate a mix, common states represent
    a DJ's style threshold or goal progress threshold.
    Can represent either a min, max, "ideal" state (no range)

    For example, using features: [TEMPO, KEY, ENERGY, VALENCE]
    """

    def __init__(self, values: numpy.array):
        """
        Initializes a threshold instance
        """
        self.data = values
    
    def get_data(self) -> numpy.array:
        """
        Returns the data for this SongVector object
        """
        return self.data