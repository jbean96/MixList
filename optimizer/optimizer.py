import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', 'MixList'))
sys.path.append(lib_path)
from analyzer.analyzer.song import Song
from . import song_vector
from . import transition
from . import threshold
from . import mix
from . import mix_goal

class Optimizer(object):
    """ 
    Computes optimal mixtape based on given songs, transitions, style and goals.
    version 1: consider only song sequences == 2
    version 2: consider song sequences >= 2 or potentially entire "goal" sections
    """
    def __init__(self, songs, transitions, style, goals):
        """
        Initializes an Optimizer object using given params.

        Keyword args:
        """
        # check arguments are valid
        self.songs = list()

        # loop through given songs and create song vectors
        for s in songs:
            assert isinstance(s, Song)
            self.songs.append()

        self.transitions = transitions
        self.style = style
        self.goals = goals
        self.curr_goal = goals[0]
        self.songs_played = set()

    def mix_songs(self, a, b):
        """
        Compares two songs a and b based on properties of song skeleton.
        Returns a mix_sequence object representing the difference between the two songs
        in order.
        
        Keyword args:
        """
        return NotImplementedError()

    def eval_transition(self, a, b, t):
        """
        Returns the mix_sequence between two songs evaluated for a specific transition.

        Keyword args:
        """
        return NotImplementedError()

    def compare_threshold(self, mix, threshold):
        """
        Determines if mix is valid within threshold.

        Keyword args:
        """
        return NotImplementedError()

    def get_next_possibilities(self, a):
        """
        Returns a list of possible next songs given song a

        Keyword args:
        """

    def generate_mixtape(self):
        """
        Generates a mixtape using this optimizer's state.

        Keyword args:        
        """
        # choose the first song (closest to initial goal, based on song comparison)
        # while more songs && more goals
            # consider state
            # consider possibilities
                # all songs --> compare to current --> results_1
                # results_1 --> progress to goal threshold --> r_2 
                # r_2 --> evaluate transitions --> progress to goal threshold --> r_3
                # r_3 --> style threshold --> possibilities
            # make decision
                # optimal or random or a little bit of both?
                # to consider:
                    # ideal style threshold
                    # ideal progress to goal threshold
            # update state
                # update songs played
                # update curr song
                # time to next goal
            # check goal progress
                # determine if moving to next goal
        return NotImplementedError()




