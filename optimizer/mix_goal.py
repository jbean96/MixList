from analyzer.analyzer import song
class MixGoal(object): 
    """
    Represents the goal index of a mix given an ideal "song"  and time.
    """
    def __init__(self, ideal_song: song.Song, time_stamp: float):
        """
        Intializes a mix_goal instance

        Keyword Arguments:
            ideal_song: a song object created with features representing the ideal sound of the mix.
            time_stamp: the time at which the ideal song should occur.
        """
        self.ideal = ideal_song
        self.time = time_stamp
    
    def get_song(self):
        """
        Returns the song for this goal.
        """
        return self.ideal
    
    def get_time(self):
        """
        Returns the time for this goal in seconds.
        """
        return self.time