from analyzer.analyzer import Song

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
        assert isinstance(song, Song)
        # convert instance of Song to a song_vector