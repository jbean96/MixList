from .threshold import Cue
from .mix import Mix
from enum import Enum
import numpy
import scipy.stats as stats

class Style(object):
    """
    Represents a DJs "style" using normal distributions and weights for each threshold feature:
    mean: [TEMPO, KEY, DANCE, ENERGY, VALENCE]
    dev: [TEMPO, KEY, DANCE, ENERGY, VALENCE]
    weight: [TEMPO, KEY, DANCE, ENERGY, VALENCE]
    TODO: add pace consistency, how often does this DJ stick to the pace?
    """

    MAX_SCORE = 10.0
    MIN_SCORE = 0.0

    def __init__(self, mean: numpy.array, deviation: numpy.array, weight: numpy.array):
        """
        Constructs a Style instance
        """ 
        self.mean = mean
        self.dev = deviation
        assert numpy.sum(weight) <= self.MAX_SCORE
        self.weight = weight
        self.distr = stats.norm
    
    def score_mix(self, mix: Mix) -> float:
        """
        Evaluates a mix based on the probability of occurence for this style.
        Higher score means high probability of occurence, 0.0 < score < 10.0

        Keyword Arguments:
            mix: the mix to be evaluated against this Style.
        """
        score = 0.0
        # for each feature: distr(mix_value, feature_mean, feature_deviation) * feature_weight
        for feature in Cue:
            if not numpy.isnan(mix.threshold[feature.value]):
                score += self.distr.pdf(mix.threshold[feature.value], self.mean[feature.value], self.dev[feature.value]) * self.weight[feature.value]
            else:
                score += 0.0
        return score 
    
    def mix_feature_score(self, mix: Mix, feature: Cue) -> float:
        """
        Return the score for this style for a Mix considering only a single feature WEIGHTED. Returns numpy.nan if Mix feature is numpy.nan.
        """
        if numpy.isnan(mix.threshold[feature.value]):
            return numpy.nan
        return self.distr.pdf(mix.threshold[feature.value], self.mean[feature.value], self.dev[feature.value]) * self.weight[feature.value]
    
    def __str__(self):
        return "{} : {}".format(numpy.vstack((self.mean, self.dev)), self.weight)
    
    def __repr__(self):
        return "{} : {}".format(numpy.vstack((self.mean, self.dev)), self.weight)

class Style_Lib(Enum):
    perfect_mixes = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([3, 1, 0.1, 0.1, 0.1]), numpy.array([9, 0, 0.3, 0.3, 0.3])) 
    balanced = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([10, 3, 0.2, 0.2, 0.2]), numpy.array([7, 0, 1, 1, 1]))    
    vibe_based = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([15, 6, 0.3, 0.3, 0.3]), numpy.array([4, 0, 2, 2, 2]))
    tempo_based = Style(numpy.array([0, 0, 0, 0, 0]), numpy.array([5, 0, 0.2, 0.2, 0.2]), numpy.array([9, 0, 0.1, 0.1, 0.1])) 