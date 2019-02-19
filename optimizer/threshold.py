import numpy
class Threshold(object):
    """
    Represents a "threshold" to evaluate a mix, common states represent
    a DJ's style threshold or goal progress threshold.
    Can represent either a min, max, "ideal" state (no range)

    For example, using features: []
    """

    def __init__(self, values):
        """
        Initializes a threshold instance
        """
        assert isinstance(values, numpy.ndarray)
        self.data = values
    
    def get_data(self) -> numpy.ndarray:
        """
        Returns the data for this SongVector object
        """
        return self.data