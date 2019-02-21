from . import threshold
class Style(object):
    """
    Represents a DJs "style" defined by 3 different thresholds
    min: minimum threshold for a mix
    max: maximum threshold for a mix
    ideal: ideal characteristics of a mix
    """

    def __init__(self, min: threshold.Threshold, max: threshold.Threshold, ideal: threshold.Threshold):
        """
        Constructs a Style instance
        """ 
        self.min = min
        self.max = max
        self.ideal = ideal