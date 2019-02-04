from typing import Any, List
from fuzzywuzzy import fuzz

from .analysis import Analysis
from . import util

class Song:
    def __init__(self, track_name: str):
        self._track_name = track_name
        self._analysis = Analysis()

        self.set_analysis_feature(Analysis.Feature.NAME, track_name)

    def get_name(self) -> str:
        """
        Returns the name of this song
        """
        return self._track_name

    def analyze(self):
        """
        Fills the analysis object for this Song
        """
        pass

    def get_analysis(self) -> Analysis:
        """
        @return: The Analysis object for this song
        """
        return self._analysis

    def set_analysis_feature(self, feature: Analysis.Feature, value: Any):
        self._analysis.set_feature(feature, value)

    def get_analysis_feature(self, feature: Analysis.Feature) -> Any:
        return self._analysis.get_feature(feature)

    def similarity(self, other: 'Song', features: List[Analysis.Feature]=None) -> float:
        """
        Gets the similarity of this song to another

        @param other: The Song to compare this song to
        @param features: The Analysis.Features to compare between the two songs
        @return: A float representing the similarity of these two songs, higher value means higher similarity
        """

        comp_dict = {
            Analysis.Feature.DURATION : { 'weight' : 1.0, 'method' : util.ratio_comparison },
            Analysis.Feature.NAME : { 'weight' : 1.0, 'method' : lambda x, y: fuzz.ratio(x, y) / 100.0 },
            Analysis.Feature.TEMPO : { 'weight' : 0.5, 'method' : util.ratio_comparison }
        }

        if features is None:
            features = list(comp_dict.keys())

        max_similarity = sum(map(lambda x: x['weight'], comp_dict.values()))

        similarity = 0.0
        for feature in features:
            if feature not in comp_dict:
                raise Exception('No comparison setup for feature: %s' % feature)

            comp = comp_dict[feature]['method'](self.get_analysis_feature(feature), other.get_analysis_feature(feature))
            similarity += comp * comp_dict[feature]['weight']
        
        return similarity / max_similarity