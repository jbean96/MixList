import sys, os, numpy
lib_path = os.path.abspath(os.path.join(__file__, '..', 'MixList'))
sys.path.append(lib_path)
from analyzer.analyzer import song
from . import song_vector
from . import transition
from . import threshold
from . import mix
from . import mix_goal
from . import style

class Optimizer(object):
    """ 
    Computes optimal mixtape based on given songs, transitions, style and goals.
    version 1: consider only song sequences == 2
    version 2: consider song sequences >= 2 or potentially entire "goal" sections
    """
    def __init__(self, songs, transitions, style: style.Style, goals):
        """
        Initializes an Optimizer object using given params.

        Keyword args:
        """
        # check arguments are valid
        # loop through given songs and ensure they are valid
        self.songs = list()
        for s in songs:
            assert isinstance(s, song.Song)
            self.songs.append(s)
        # loop through given transition and ensure they are valid 
        self.transitions = list()
        for t in transitions:
            assert isinstance(t, transition.Transition)
            self.transitions.append(t)
        
        self.style = style
        # loop through given goals and ensure they are valid
        self.goals = list()
        for g in goals:
            assert isinstance(g, mix_goal.MixGoal)
            # check that the time stamps are strictly increasing
            if (len(self.goals) > 1):
                assert self.goals[len(self.goals - 1)].time < g.time
        self.curr_goal = goals[0]
        self.songs_played = set()

    def mix_songs(self, a: song.Song, b: song.Song) -> mix.MixSequence:
        """
        Compares two songs a and b based on properties of song skeleton.
        Returns a mix_sequence object representing the difference between the two songs
        in order.
        
        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
        """
        return mix.MixSequence(a, b)

    def eval_transition(self, a: song.Song, b: song.Song, t: transition.Transition) -> mix.MixSequence:
        """
        Returns the mix_sequence between two songs evaluated for a specific transition.

        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
            t: the transition to apply to the mix.
        """
        return mix.MixSequence(a, b).apply_transition(t)

    def in_threshold_range(self, mix: mix.MixSequence, min: threshold.Threshold, max: threshold.Threshold) -> bool:
        """
        Determines if mix is valid within threshold.

        Keyword args:
        """
        min_result = numpy.subtract(mix.diff, min.get_data)
        # check all elements, if < 0 then return false
        max_result = numpy.subtract(mix.diff, max.get_data) 
        # check all elements, if > 0 then return false
        return True
    
    def threshold_diff(self, mix: mix.MixSequence, ideal: threshold.Threshold) -> float:
        result = numpy.subtract(mix.diff, ideal.get_data)
        # take absolute value of all array elements
        # return the sum of results elements
        return 0.0

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




