from .threshold import Threshold
from .mix import Mix
from enum import Enum

class Style(object):
    """
    Represents a DJs "style" defined by 3 different thresholds
    min: minimum threshold for a mix
    max: maximum threshold for a mix
    ideal: ideal characteristics of a mix
    """

    def __init__(self, min: Threshold, max: Threshold, ideal: Threshold):
        """
        Constructs a Style instance
        """ 
        self.min = min
        self.max = max
        self.ideal = ideal
    
    def score_mix(self, mix: Mix) -> float:
        """
        Evaluates a mix based on this style and returns a float "score" >= 0 indicating
        how well this mix aligns with the style, a higher score means better mix.

        Keyword Arguments:
            mix: the mix to be evaluated against this Style.
        """
        return 0.0

class Style_Lib(Enum):
    conservative = Style(Threshold([0, 0, 0, 0, 0]), Threshold([5, 2, 0.2, 0.2, 0.2]), Threshold([0, 0, 0, 0, 0]))
    regular = Style(Threshold([0, 0, 0, 0, 0]), Threshold([10, 4, 0.5, 0.5, 0.5]), Threshold([0, 1, 0.1, 0.1, 0.1]))
    loose = Style(Threshold([0, 0, 0, 0, 0]), Threshold([15, 8, 0.8, 0.8, 0.8]), Threshold([3, 3, 0.2, 0.2, 0.2]))