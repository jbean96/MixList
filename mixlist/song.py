from typing import Any, List
from fuzzywuzzy import fuzz

from mixlist.analysis import Analysis

class Song:
    def __init__(self, track_name: str):
        self._track_name = track_name
        self._analysis = Analysis()

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

    def similarity(self, other: 'Song', features: List[Analysis.Feature]) -> float:
        """
        Gets the similarity of this song to another

        @param other: The Song to compare this song to
        @param features: The Analysis.Features to compare between the two songs
        @return: A float representing the similarity of these two songs, higher value means higher similarity
        """
        name_comp = fuzz.ratio(self.get_name(), other.get_name()) / 100.0
        
        pass