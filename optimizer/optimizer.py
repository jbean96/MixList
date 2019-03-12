import sys, os, numpy, random
lib_path = os.path.abspath(os.path.join(__file__, '..', 'MixList'))
sys.path.append(lib_path)
from analyzer import song
from analyzer import analysis
from .transition import Transition
from .threshold import Threshold
from .mix import Mix
from .mix import Comp
from .mix_goal import MixGoal
from .style import Style
from typing import Dict
from typing import List
from typing import Set

class Optimizer(object):
    """ 
    Computes optimal mixtape based on given songs, transitions, style and goals.
    version 1: consider only song sequences == 2
    version 2: consider song sequences >= 2 or potentially entire "goal" sections
    TODO: create mixes by comparing songs on a more complex feature set
    TODO: create and parameterize a library of high level transitions
    TODO: create a library of different "styles"
    TODO: generate mixes using up to N length song sequences
    """
    def __init__(self, songs: List[song.Song], goals: List[MixGoal], transitions: List[Transition]=None, style: Style=None):
        """
        Initializes an Optimizer object using given params.

        Keyword args:
            songs: list of Song objects to create the mixtape.
            goals: list of MixGoal objects to guide the construction of the mixtape.
            transitions: list of transitions available to use in the creation of the mixtape.
            style: style of the DJ used to influence mixtape creation. 
        """
        # check arguments are valid

        # Validate songs.
        self.songs = set()
        for s in songs:
            assert isinstance(s, song.Song)
            self.songs.add(s)

        # Validate goals.
        self.goals = list()
        for g in goals:
            assert isinstance(g, MixGoal)
            # check that the time stamps are strictly increasing
            if (len(self.goals) > 1):
                assert self.goals[len(self.goals - 1)].get_time() < g.get_time()
            # insert the goal
            self.goals.append(g)

        # Validate style (might be none).
        if style is not None:
            self.style = style
        
        # Validate transitions (might be none).
        self.transitions = set()
        if transitions is not None:
            for t in transitions:
                assert isinstance(t, Transition)
                self.transitions.add(t)

        # initialize the current goal to be the first goal given
        self.curr_goal = goals[0]
        # no songs have been played in this SET (pun-intended)
        self.songs_played = set()

    def get_next_possibilities(self, a) -> Set[Mix]:
        """
        Returns a list of possible next songs from unplayed songs given a.
        If there are no unplayed songs then return None.

        Keyword args:
        """
        # consider possibilities
            # all songs --> compare to current --> results_1
            # results_1 --> progress to goal threshold --> r_2 
            # r_2 --> evaluate transitions --> progress to goal threshold --> r_3
            # r_3 --> style threshold --> possibilities
        unplayed_songs = self.songs - self.songs_played
        if (len(unplayed_songs) == 0):
            # if all songs have been played then return None
            return None

        # initialize possible mixes
        possible_mixes = set()

        # generate all possible mixes
        for song in unplayed_songs:
            possible_mixes.add(self.mix_songs(a, song))


        if len(self.transitions) > 0:
            # generate all possible mixes using one transition
            possible_mixes_t = set()
            for p in possible_mixes:
                for t in self.transitions:
                    possible_mixes_t.add(p.apply_transition(t))
            possible_mixes = possible_mixes_t

        return possible_mixes

    def generate_mixtape(self) -> List:
        """
        Generates a mixtape using this optimizer's state.
        Keyword args:        
        """
        # choose the first song (closest to initial goal, based on song comparison)
        """ 
        first_mix_options = set()
        for s in self.songs:
           first_mix_options.add(self.mix_songs(self.curr_goal.get_song(), s)) 
        
        # find the song closest in tempo
        first_mix = first_mix_options.pop()
        for f in first_mix_options:
            if abs(f.comp_vector[Comp.TEMPO.value]) < abs(first_mix.comp_vector[Comp.TEMPO.value]):
                first_mix = f
        """ 
        # first song chosen is random
        curr_song = random.sample(self.songs, 1)[0]
        # add the first song to played
        self.songs_played.add(curr_song)
        # find all the songs that have not yet been played
        unplayed_songs = self.songs - self.songs_played
        # initialize an empty list
        mix_list = list()
        # add curr song to the list
        mix_list.append(curr_song)

        # order the songs based on tempo
        while (len(unplayed_songs) > 0):
            possible = self.get_next_possibilities(curr_song)
            # choosed next song based on closest tempo
            assert len(possible) > 0
            next_mix = possible.pop()
            for m in possible:
                if abs(m.comp_vector[Comp.TEMPO.value]) < abs(next_mix.comp_vector[Comp.TEMPO.value]):
                    next_mix = m
            self.songs_played.add(next_mix.track_b)
            curr_song = next_mix.track_b
            mix_list.append(curr_song)
            unplayed_songs.remove(next_mix.track_b)
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
        return self.generate_basic_mix_script(mix_list)
    
    @staticmethod
    def generate_basic_mix_script(mix_list: List[song.Song]) -> List:
        """
        Takes a list of Song objects and convert it to a mix script using a simple transition.
        """
        mix_script = list()
        # pass transition type
        t_1 = "crossfade"
        t_2 = "tempomatch"
        # transition is length is always 16 
        length = 32
        # curr song
        curr_song = mix_list.pop(0)
        # while there are still songs in the mix list 
        while(len(mix_list) > 0):
            start_a = len(curr_song.get_analysis_feature(analysis.Feature.BEATS)) - 33
            next_song = mix_list.pop(0)
            song_a_text = "{} - {}".format(curr_song.get_analysis_feature(analysis.Feature.NAME), curr_song.get_analysis_feature(analysis.Feature.TEMPO))
            song_b_text = "{} - {}".format(next_song.get_analysis_feature(analysis.Feature.NAME), next_song.get_analysis_feature(analysis.Feature.TEMPO))
            curr_script = {"song_a": curr_song,  "song_b": next_song, "start_a": start_a, "start_b": 0, "sections":
                            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                          }
            curr_song = next_song
            mix_script.append(curr_script)
        return mix_script

        """
        TODO:
        Guarantee: effects list and transition list are in the same order.
        effects_list = {UserSong: [effect_1, effect_2, ...]}
        effect: {start_offset: integer, end_offset: integer, type: effect_type}
        """

    @staticmethod
    def mix_songs(a: song.Song, b: song.Song) -> Mix:
        """
        Compares two songs a and b based on properties of song skeleton.
        Returns a mix_sequence object representing the difference between the two songs
        in order.
        
        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
        """
        return Mix(a, b)

    @staticmethod
    def eval_transition(a: song.Song, b: song.Song, t: Transition) -> Mix:
        """
        Returns the mix_sequence between two songs evaluated for a specific transition.

        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
            t: the transition to apply to the mix.
        """
        return Mix(a, b).apply_transition(t)

    @staticmethod
    def in_threshold_range(mix: Mix, min: Threshold, max: Threshold) -> bool:
        """
        Determines if mix is valid within threshold.

        Keyword args:
        """
        min_result = numpy.subtract(mix.diff, min.get_data)
        # check all elements, if < 0 then return false
        assert isinstance(min_result, numpy.array)
        if numpy.any(min_result[:, 0] < 0):
            return False
        max_result = numpy.subtract(mix.diff, max.get_data) 
        assert isinstance(max_result, numpy.array)
        if numpy.any(max_result[:, 0] > 0):
            return False
        # check all elements, if > 0 then return false
        return True

    @staticmethod 
    def threshold_diff(mix: Mix, ideal: Threshold) -> float:
        result = numpy.subtract(mix.diff, ideal.get_data)
        # take absolute value of all array elements
        # return the sum of results elements
        return numpy.absolute(result)

    @staticmethod
    def generate_3_track(a: song.Song, b: song.Song, c: song.Song) -> List:
        """
        For testing purposes.
        Returns a structure ready for the composer that represents a mix between
        Song a --> Song b --> Song c using 16 beat crossfade/tempochange transition.
        """
        # get beat 16 beats from the end of Song a for transition 2
        beat_a_0 = len(a.get_analysis_feature(analysis.Feature.BEATS)) - 33
        # start beat 0 for Song b on transition 0
        beat_b_0 = 0
        # start beat 16 beats from end of Song b for transition 1
        beat_b_1 = len(b.get_analysis_feature(analysis.Feature.BEATS)) - 33
        # start beat 0 for Song c on transition 1
        beat_c_1 = 0
        # transition is length is always 16
        length = 32
        # pass transition type
        t_1 = "crossfade"
        t_2 = "tempomatch"
        mix = [
                {"song_a": a, "song_b": b, "start_a": beat_a_0,"start_b": beat_b_0, "sections":
                    [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                },
                {"song_a": b, "song_b": c, "start_a": beat_b_1, "start_b": beat_c_1, "sections":
                    [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                }
            ]
        return mix