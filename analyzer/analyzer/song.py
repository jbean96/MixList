from enum import auto, Enum
from fuzzywuzzy import fuzz
from typing import Any, List
import pdb

from . import analysis
from . import util

class Song:
    def __init__(self, track_name: str):
        self._track_name = track_name
        self._analysis = analysis.Analysis()

        self.set_analysis_feature(analysis.Feature.NAME, track_name)

    def get_name(self) -> str:
        """
        @return: The name of the song
        """
        return self._track_name

    def is_analyzed(self, feature: analysis.Feature) -> bool:
        """
        @return: True if the Song has been analyzed, False otherwise
        """
        return self._analysis is not None and self._analysis.is_analyzed(feature)

    def analyze(self):
        """
        Fills the analysis object for this Song
        """
        pass

    def get_analysis(self) -> analysis.Analysis:
        """
        @return: The Analysis object for this song
        """
        return self._analysis

    def set_analysis_feature(self, feature: analysis.Feature, value: Any):
        self._analysis.set_feature(feature, value)

    def get_analysis_feature(self, feature: analysis.Feature) -> Any:
        return self._analysis.get_feature(feature)

def similarity(song1: Song, song2: Song, features: List[analysis.Feature]=None) -> float:
    """
    Gets the similarity of this song to another

    @param song1: The first song to compare, will do mathematcial ratios using this songs 
        feature value as the denominator
    @param song2: The second song to compare
    @param features: The analysis.Features to compare between the two songs, if None then
        all possible comparison features will be used, default is None
    @return: A float representing the similarity of these two songs, higher value means 
        higher similarity
    @raise: Exception if a specified feature isn't setup for comparison yet
    """
    comp_dict = {
        analysis.Feature.DURATION : { 'weight' : 1.0, 'method' : lambda x, y: util.ratio_comparison(x, y, exp=1.1) },
        # analysis.Feature.NAME : { 'weight' : 0.3, 'method' : lambda x, y: fuzz.ratio(x, y) / 100.0 },
        analysis.Feature.TEMPO : { 'weight' : 0.7, 'method' : util.ratio_comparison }
    }

    if features is None:
        features = list(comp_dict.keys())

    max_similarity = sum(map(lambda x: x['weight'], comp_dict.values()))

    similarity = 0.0
    for feature in features:
        if feature not in comp_dict:
            raise Exception('No comparison setup for feature: %s' % feature)

        comp = comp_dict[feature]['method'](song1.get_analysis_feature(feature), 
            song2.get_analysis_feature(feature))
        similarity += comp * comp_dict[feature]['weight']
    
    return similarity / max_similarity