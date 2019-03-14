class MixGoal(object): 
    """
    Represents a high level mix section given 4 ideal characteristics 0.0 <= and >= 10.0 and time.
    energy (wild <--> chillin') 
    danceability (groovy <--> awkward)
    valence (happy <--> sad)
    pace (fast <--> slow)
    time (when should this happen?)
    """
    def __init__(self, energy: float, danceability: float, valence: float, pace: float, time_stamp: float):
        """
        Intializes a mix_goal instance
        """
        assert energy >= 0.0 and energy <= 10.0
        assert danceability >= 0.0 and danceability <= 10.0
        assert valence >= 0.0 and valence <= 10.0
        assert pace >= 0.0 and pace <= 10.0
        self.energy = energy
        self.dance = danceability
        self.valence = valence
        self.pace = pace
        self.time = time_stamp