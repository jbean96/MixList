from typing import Any

from mixlist.analysis import Analysis

class Song:
    def __init__(self, track_name):
        self._track_name = track_name
        self._analysis = Analysis()

    def get_name(self):
        """
        Returns the name of this song
        """
        return self._track_name

    def get_analysis(self):
        return self._analysis

    def set_analysis_feature(self, feature: Analysis.Feature, value: Any):
        self._analysis.set_feature(feature, value)

    def get_analysis_feature(self, feature: Analysis.Feature) -> Any:
        return self._analysis.get_feature(feature)

    def similarity(self, other: 'Song') -> float:
        """
        Gets the similarity of this song to another

        @param other: The Song to compare this song to
        @return: A float representing the similarity of these two songs, higher value means higher similarity
        """
        pass