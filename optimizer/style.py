from .threshold import Cue
from .mix import Mix
from enum import Enum
import numpy

class Score_Weight(Enum):
    TEMPO = 10.0
    KEY = 0.0
    DANCE = 0.0
    ENERGY = 0.0
    VALENCE = 0.0

class Style(object):
    """
    Represents a DJs "style" defined by 3 different thresholds
    min: minimum threshold for a mix
    max: maximum threshold for a mix
    ideal: ideal characteristics of a mix
    """

    def __init__(self, min: numpy.array, max: numpy.array, ideal: numpy.array):
        """
        Constructs a Style instance
        """ 
        self.min = min
        self.max = max
        self.ideal = ideal
    
    def score_mix(self, mix: Mix) -> float:
        """
        Evaluates a mix based on this style and returns a float 0 <= score <= 10 indicating
        how well this mix aligns with the style, a lower score means better mix.
        Ensures transitions fall within the min and max, then scores based on ideal.

        Keyword Arguments:
            mix: the mix to be evaluated against this Style.
        """
        min_result = numpy.subtract(mix.comp_vector, self.min)
        # check if any changes are below the min
        if numpy.any(min_result[Cue.TEMPO.value:] < 0):
            return 10.0
        max_result = numpy.subtract(mix.comp_vector, self.max)
        # check if any changes are above the max
        if numpy.any(max_result[Cue.TEMPO.value:] < 0):
            return 10.0
        
        score = 0.0
        ideal_compare = numpy.absolute(numpy.subtract(mix.comp_vector, self.ideal))
        # normalize the score
        score += (ideal_compare[Cue.TEMPO.value] / self.ideal.get_data()[Cue.TEMPO.value]) * Score_Weight.TEMPO
        score += (ideal_compare[Cue.KEY.value]  / self.ideal.get_data()[Cue.KEY.value]) * Score_Weight.KEY
        score += (ideal_compare[Cue.DANCE.value] / self.ideal.get_data()[Cue.DANCE.value]) * Score_Weight.DANCE
        score += (ideal_compare[Cue.ENERGY.value] / self.ideal.get_data()[Cue.ENERGY.value]) * Score_Weight.ENERGY
        score += (ideal_compare[Cue.VALENCE.value] / self.ideal.get_data()[Cue.VALENCE]) * Score_Weight.VALENCE

        return score 

class Style_Lib(Enum):
    conservative = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([5, 2, 0.2, 0.2, 0.2]), numpy.array([0, 0, 0, 0, 0]))
    regular = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([10, 4, 0.5, 0.5, 0.5]), numpy.array([0, 1, 0.1, 0.1, 0.1]))
    loose = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([15, 8, 0.8, 0.8, 0.8]), numpy.array([3, 3, 0.2, 0.2, 0.2]))