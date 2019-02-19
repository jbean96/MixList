import numpy
from analyzer.analyzer import song
from analyzer.analyzer import analysis

class SongVector(object):
    """
    Transforms data from a "song" object given by the analyzer into a song_vector
    for easy comparison and manipulation through vector/matrix calculations
    during the optimization process
    """

    def __init__(self, song):
        """
        Initializes a song vector instance
        """
        assert isinstance(song, song.Song)
        # convert instance of Song to a song_vector
        # tempo, key, energy, valence (happy vs. sad)
        if song.isAnalyzed():
            self.data = numpy.ndarray([
                song.get_analysis().get_feature(song.Feature.TEMPO),
                song.get_analysis().get_feature(song.Feature.KEY),
                song.get_analysis().get_feature(song.Feature.ENERGY),
                song.get_analysis().get_feature(song.Feature.VALENCE)
            ])
        else:
            AssertionError("Song passed to initialize a SongVector must be analyzed.")
    
    def get_data(self) -> numpy.ndarray:
        """
        Returns the data for this SongVector object
        """
        return self.data