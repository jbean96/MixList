from mixlist.song import Song

class song_vector():
    """
    Transforms data from a "song" object given by the analyzer into a song_vector
    for easy comparison and manipulation through vector/matrix calculations
    during the optimization process

    """

    def __init__(self, song):
        """

        Initializes a song vector instance
        
        """
        # convert instance of Song to a song_vector