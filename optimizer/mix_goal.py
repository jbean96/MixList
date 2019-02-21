from analyzer.analyzer import song
class MixGoal(object): 
    """
    Represents the goal index of a mix given an ideal "song"  and time.
    """
    def __init__(self, ideal_song: song.Song, time_stamp: float):
        """
        Intializes a mix_goal instance
        """
        # a mix goal is a tuple with a Song and a TimeStamp (float in seconds)
        self.ideal = ideal_song
        self.time = time_stamp