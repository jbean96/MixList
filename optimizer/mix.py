import numpy, sys, os
from analyzer.song import Song
from analyzer.analysis import Feature
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..")))
from optimizer.mix_goal import MixGoal

class Mix(object):
    """
    Represents a mix between a sequence of songs in the order
    Initially two, later >= 2

    TODO: create a method for converting the given mix object to a script for composer.
    Later version features:
        - consider different sections of each song
        - consider multiple songs
    TODO: add the ability to initialize with a song and a MixGoal, allowing the DJ to interpret
    the goals --> turn this into a boolean feature?
    """
    def __init__(self, track_a: Song, track_b: Song):
        """
        Keyword Args:
            track_a: a Song instance representing the starting song in this mix.
            track_b: a Song instance representing the end song in this mix.
        
        Initializes a new Mix instance with no transition history, compares the start
        and end song without factoring in a transition.
        """
        self.track_a = track_a
        self.track_b = track_b
        # compute difference between the two song vectors
        self.threshold = self.__compare_songs(self.track_a, self.track_b)
    
    @classmethod
    def compare_song_to_goal(self, song: Song, goal: MixGoal) -> 'Mix':
        """
        Creates a valid Mix instace using the shared attributes of a Song and MixGoal.
        
        Allows the DJ's Style to make decisions about the adherence to the MixGoals.
        """
        # TODO: implement this
        raise NotImplementedError()

    def __compare_songs(self, track_a: Song, track_b: Song) -> numpy.array:
        """
        Returns a numpy array that represents the comparison vector between track_a
        into track_b in the form:
        [TEMPO_DIFF, KEY_DIFF, DANCE_DIFF, ENERGY_DIFF, VALENCE_DIFF]
        If any feature for either Song in a comparison is not analyzed that index will be NaN
        """
        # compare tempo
        tempo_diff = track_b.get_analysis_feature(Feature.TEMPO) - track_a.get_analysis_feature(Feature.TEMPO)
        # compare key
        # get the distance between keys according to the Camelot wheel.
        key_diff = numpy.nan
        # compare danceability
        dance_diff = track_b.get_analysis_feature(Feature.DANCEABILITY) - track_a.get_analysis_feature(Feature.DANCEABILITY)
        # compare energy
        energy_diff = track_b.get_analysis_feature(Feature.ENERGY) - track_a.get_analysis_feature(Feature.ENERGY) 
        # compare valence
        val_diff = track_b.get_analysis_feature(Feature.VALENCE) - track_a.get_analysis_feature(Feature.VALENCE)
        # return comparison vector
        return numpy.array([tempo_diff, key_diff, dance_diff, energy_diff, val_diff])