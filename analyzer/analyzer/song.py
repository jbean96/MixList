import eyed3.id3
from enum import auto, Enum
from typing import Any, List

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

    def get_id3(self) -> eyed3.id3.tag.Tag:
        return None

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
    
    def set_analysis(self, analysis_obj: analysis.Analysis):
        """
        Sets the analysis for this song to a externally created Analysis object;
        should only be used for testing
        """
        self._analysis = analysis_obj
        self._is_internally_analyzed = True

    def set_analysis_feature(self, feature: analysis.Feature, value: Any):
        self._analysis.set_feature(feature, value)

    def get_analysis_feature(self, feature: analysis.Feature) -> Any:
        return self._analysis.get_feature(feature)
    
    def __str__(self):
        return "{} : {}".format(self.get_analysis_feature(analysis.Feature.NAME), self.get_analysis_feature(analysis.Feature.TEMPO))
    
    def __repr__(self):
        return "{} : {}".format(self.get_analysis_feature(analysis.Feature.NAME), self.get_analysis_feature(analysis.Feature.TEMPO))

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
        analysis.Feature.TEMPO : { 'weight' : 0.7, 'method' : lambda x, y: util.ratio_comparison(x, y, exp=1.2) }
    }

    if features is None:
        features = list(comp_dict.keys())

    max_similarity = sum(map(lambda x: x['weight'], comp_dict.values()))

    similarity = 0.0
    for feature in features:
        if feature not in comp_dict:
            raise Exception('No comparison setup for feature: %s' % feature)

        # If one of the songs just doesn't have it analyzed...
        # TODO: Should it just set 0 for that comparison score?
        if not song1.is_analyzed(feature) or not song2.is_analyzed(feature):
            raise Exception("Feature %s is not analyzed for at least one of the songs being compared" % feature)
        comp = comp_dict[feature]['method'](song1.get_analysis_feature(feature), 
            song2.get_analysis_feature(feature))
        similarity += comp * comp_dict[feature]['weight']
    
    return similarity / max_similarity