import sys, os, numpy
lib_path = os.path.abspath(os.path.join(__file__, '..', 'MixList'))
sys.path.append(lib_path)
from analyzer.analyzer import song
from analyzer.analyzer import analysis
from . import transition
from . import threshold
from . import mix
from . import mix_goal
from . import style
from typing import Dict
from typing import List
from typing import Set

class Optimizer(object):
    """ 
    Computes optimal mixtape based on given songs, transitions, style and goals.
    version 1: consider only song sequences == 2
    version 2: consider song sequences >= 2 or potentially entire "goal" sections
    """
    def __init__(self, songs: List[song.Song], transitions: List[transition.Transition], style: style.Style, goals: List[mix_goal.MixGoal]):
        """
        Initializes an Optimizer object using given params.

        Keyword args:
        """
        # check arguments are valid

        # loop through given songs and ensure they are valid
        self.songs = set()
        for s in songs:
            assert isinstance(s, song.Song)
            self.songs.add(s)

        # loop through given transition and ensure they are valid 
        self.transitions = set()
        for t in transitions:
            assert isinstance(t, transition.Transition)
            self.transitions.add(t)
        
        self.style = style

        # loop through given goals and ensure they are valid
        self.goals = list()
        for g in goals:
            assert isinstance(g, mix_goal.MixGoal)
            # check that the time stamps are strictly increasing
            if (len(self.goals) > 1):
                assert self.goals[len(self.goals - 1)].time < g.time
            # insert the goal
            self.goals.append(g)

        self.curr_goal = goals[0]
        self.songs_played = set()

    def get_next_possibilities(self, a) -> Set[mix.Mix]:
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
            return None

        possible_mixes = set()

        # generate all possible mixes
        for song in unplayed_songs:
            possible_mixes.add(self.mix_songs(a, song))

        possible_mixes_t = set()

        # generate all possible mixes using one transition
        """
        for p in possible_mixes:
            for t in self.transitions:
                possible_mixes_t.add(p.apply_transition(t))
        """ 
        return possible_mixes

    def generate_mixtape(self) -> List[song.Song]:
        """
        Generates a mixtape using this optimizer's state.

        Keyword args:        
        """
        # choose the first song (closest to initial goal, based on song comparison)
        first_mix_options = set()
        for s in self.songs:
           first_mix_options.add(self.mix_songs(self.curr_goal, s)) 
        
        # find the song closest in tempo
        first_mix = first_mix_options.pop()
        for f in first_mix_options:
            if abs(f.comp_vector[0]) < abs(first_mix.comp_vector[0]):
                first_mix = f
        
        self.songs_played.add(first_mix.track_b)
        curr_song = first_mix.track_b
        unplayed_songs = self.songs - self.songs_played
        mix_list = list()
        mix_list.append(curr_song)

        # order the songs based on tempo
        while (len(unplayed_songs) > 0):
            possible = self.get_next_possibilities(curr_song)
            # choosed next song based on closest tempo
            assert len(possible) > 0
            next_mix = possible.pop()
            for m in possible:
                if abs(m.comp_vector[0]) < abs(next_mix.comp_vector[0]):
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
            start_a = len(curr_song.get_analaysis_feature(analysis.Feature.BEATS)) - 33
            next_song = mix_list.pop(0)
            curr_script = {"song_a": curr_song, "song_b": next_song, "start_a": start_a, "start_b": 0, "sections":
                            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                          }
            curr_song = next_song
            mix_script.append(curr_script)
        return NotImplementedError()

        """
        Guarantee: effects list and transition list are in the same order.
        effects_list = {UserSong: [effect_1, effect_2, ...]}
        effect: {start_offset: integer, end_offset: integer, type: effect_type}
        """

    @staticmethod
    def mix_songs(a: song.Song, b: song.Song) -> mix.Mix:
        """
        Compares two songs a and b based on properties of song skeleton.
        Returns a mix_sequence object representing the difference between the two songs
        in order.
        
        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
        """
        return mix.Mix(a, b)

    @staticmethod
    def eval_transition(a: song.Song, b: song.Song, t: transition.Transition) -> mix.Mix:
        """
        Returns the mix_sequence between two songs evaluated for a specific transition.

        Keyword args:
            a: the first song to be mixed fo Song type.
            b: the second song to be mixed of Song type.
            t: the transition to apply to the mix.
        """
        return mix.Mix(a, b).apply_transition(t)

    @staticmethod
    def in_threshold_range(mix: mix.Mix, min: threshold.Threshold, max: threshold.Threshold) -> bool:
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
    def threshold_diff(mix: mix.Mix, ideal: threshold.Threshold) -> float:
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