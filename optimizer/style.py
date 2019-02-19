from . import transition
class Style(object):
    """
    Represents a DJs "style" by representing their preferences as 3 thresholds
    min: minimum threshold for a mix
    max: maximum threshold for a mix
    ideal: ideal characteristics of a mix
    """

    def __init__(self, min: transition.Transition, max: transition.Transition, ideal: transition.Transition):
        """
        Constructs a Style instance
        """ 
        self.min = min
        self.max = max
        self.ideal = ideal