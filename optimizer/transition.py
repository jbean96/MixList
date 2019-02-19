import numpy
class Transition(object):
    """
    Represents a "transition" between two songs as a vector, can be applied to a mix
    to modify different features of the mix based on the interpretted effect of the transition.
    
    [TEMPO SCALAR, KEY DIFF SCALAR, ENERGY SCALAR, VALENCE SCALAR]
    """
    def __init__(self, values: numpy.ndarray):
        """
        Creates a new transition object.
        """
        self.data = numpy.ndarray
    
    def get_data(self) -> numpy.ndarray:
        """
        Returns the data for this Transition object.
        """
        return self.data