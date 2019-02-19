class MixGoal(object): 
    """
    Represents the goal index of a mix given an ideal "song"  and time.
    """
    def __init__(self, ideal_song, time_stamp):
        """
        Intializes a mix_goal instance
        """
        # a mix goal is a tuple with a SongVector and a TimeStamp (float in seconds)
        self.data = (ideal_song, time_stamp)
    
    def get_data(self) -> tuple:
        """
        Returns the data for this MixGoal object.
        """
        return self.data