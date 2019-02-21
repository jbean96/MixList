import numpy
class Transition(object):
    """
    Represents a "transition" between two songs as a vector, can be applied to a mix
    to modify different features of the mix based on the interpretted effect of the transition.
    
    [TEMPO SCALAR, KEY DIFF SCALAR, DANCEABILITY SCALAR, ENERGY SCALAR, VALENCE SCALAR]
    """
    def __init__(self, values: numpy.array):
        """
        Creates a new transition object.
        """
        self.data = numpy.array
    
    def get_data(self) -> numpy.array:
        """
        Returns the data for this Transition object.
        """
        return self.data