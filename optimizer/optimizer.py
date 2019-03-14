import sys, os, numpy, random, math
lib_path = os.path.normpath(os.path.join(os.path.realpath(__file__), '..', '..'))
sys.path.append(lib_path)
from analyzer.song import Song
from analyzer.analysis import Feature
from analyzer import usersong
from optimizer.transition import Transition
from optimizer.threshold import Cue
from optimizer.mix import Mix
from optimizer.mix_goal import MixGoal
from optimizer.style import Style
from typing import Dict
from typing import List
from typing import Set
from composer.audio_effect_types import Transition_Types
from composer.audio_effect_types import Effect_Types

class Optimizer(object):
    """ 
    Computes optimal mixtape based on given songs, transitions, style and goals.
    version 1: consider only song sequences == 2
    version 2: consider song sequences >= 2 or potentially entire "goal" sections
    TODO: add parameter for the number of songs in a mixtape
    TODO: add parameter for the start song
    TODO: create mixes by comparing songs on a more complex feature set
    TODO: create and parameterize a library of high level transitions
    TODO: create a library of different "styles"
    TODO: generate mixes using up to N length song sequences
    TODO: change the options for factoring in Style, currently --> calculate every Mix and compare to style
        choose a feature from style (based on priority) --> choose a style value, make only mixes in that range
        choose the next feature (based on priority or random) --> choose a style value, select only mixes in that range from previous
        etc..
    """
    def __init__(self, songs: List[usersong.UserSong], goals: List[MixGoal], style: Style):
        """
        Initializes an Optimizer object using given params.

        Keyword args:
            songs: list of UserSong objects to create the mixtape.
            goals: list of MixGoal objects to guide the construction of the mixtape.
            style: Style of the DJ used to influence mixtape creation. 
        """
        # Validate UserSong objects.
        self.library = set() 
        # ***DJ PUN AIRHORN***

        for s in songs:
            assert isinstance(s, usersong.UserSong)
            self.library.add(s)

        # Validate goals.
        self.goals = list()
        for g in goals:
            assert isinstance(g, MixGoal)
            # check that the time stamps are strictly increasing
            if (len(self.goals) > 1):
                assert self.goals[len(self.goals - 1)].time < g.time
            # insert the goal
            self.goals.append(g)

        # Make sure this DJ's legit.
        assert isinstance(style, Style)
        self.style = style

        # statically programmed mixtape length
        self.mixtape_length = len(self.library)

    def get_possible_mixes(self, curr_song: Song, played_songs: Set[Song], max_results=2) -> Set[tuple]:
        """
        Returns all possible (Mix, style_score) Tuples given curr_song and all unplayed songs 
        according to this DJ's style. If there are no unplayed songs then return None.
        """
        # consider possibilities
            # all songs --> compare to current --> results_1
            # results_1 --> progress to goal threshold --> r_2 
            # r_2 --> evaluate transitions --> progress to goal threshold --> r_3
            # r_3 --> style threshold --> possibilities

        if (len(played_songs) == len(self.library)):
            # if all songs have been played then return None
            return None

        # get ready to start thinking really hard...
        possible_mixes = set()
        unplayed_songs = self.library - played_songs

        # generate all possible mixes just comparing songs
        for song in unplayed_songs:
            possible_mixes.add(self.mix_songs(curr_song, song))
        
        # consider your STYLE
        scored_mixes = [(m, self.style.score_mix(m)) for m in possible_mixes]
        # only play your best mixes live 
        scored_mixes.sort(key=lambda tup: tup[1], reverse=True)
        # return <= max_results possible mixes
        cutoff = min(len(scored_mixes), max_results)
        possible_mixes = scored_mixes[:cutoff]

        """
        for mix_to_add in possible_mixes:
            print("[{}] -> [{} : {}] -> [{}]".format(mix_to_add[0].track_a, mix_to_add[0].threshold, mix_to_add[1], mix_to_add[0].track_b))
        """

        return possible_mixes

    def generate_mixtape(self) -> List:
        """
        Generates a mixtape using this Optimizer's state.
        """
        # choose the first song (closest to initial goal, based on song comparison)
        """ 
        first_mix_options = set()
        for s in self.songs:
           first_mix_options.add(self.mix_songs(self.curr_goal.get_song(), s)) 
        
        # find the song closest in tempo
        first_mix = first_mix_options.pop()
        for f in first_mix_options:
            if abs(f.threshold[Comp.TEMPO.value]) < abs(first_mix.threshold[Comp.TEMPO.value]):
                first_mix = f
        """ 

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

        # v2 algorithm:
            # for each path between goals create a small mixtape based on two goals:
            # high level --> do a DFS between "goals" to find the best possible mix path, then create the transitions to fit the mix path.
                # if this is the first goal then choose a song closest to the goal (use get next possibilities)
                # choose an end song that is closest to the end goal (use get next possibilities)
                # get the time between this goal and end goal, convert that to a number of songs based on "pace"
                # generate the best possible mix path for that number of songs
                # decide the time to complete transition based on the pace consistency
                # decide the optimial transition

        # no songs have been played in this SET ***DJ PUN AIRHORN***
        set_list = set()
        # the truth:
        curr_song = random.sample(self.library, 1)[0]
        # make sure we know what we played
        set_list.add(curr_song)
        # hit "record" in your DJ software
        mix_list = list()
        # the current state of the mixtape: (song, set, mix, score)
        mixtapes_to_finish = [(curr_song, set_list, mix_list, 0.0)]
        complete_mixtapes = []
        # TODO: update this condition to factor in goals, otherwise we're never leaving this party.
        while len(mixtapes_to_finish) > 0:
            # decide the possible next mixes...
            curr_state = mixtapes_to_finish.pop(0)
            possible = self.get_possible_mixes(curr_state[0], curr_state[1])
            # make sure to take your headphones off once in a while
            for scored_mix in possible:
                next_song = scored_mix[0].track_b
                # don't commit the cardinal sin #norepeats
                next_set_list = set(curr_state[1])
                next_set_list.add(next_song)
                # WOAH sick mix ~bro~ better upload that to SoundCloud
                next_mix_list = list(curr_state[2])
                next_mix_list.append(scored_mix[0])
                # update the mix_list score
                next_mix_score = curr_state[3] + scored_mix[1]
                new_state = (next_song, next_set_list, next_mix_list, next_mix_score)
                # specified mixtape length reached
                if len(next_set_list) == self.mixtape_length:
                    complete_mixtapes.append(new_state)
                else:
                    print(len(next_set_list))
                    mixtapes_to_finish.append(new_state)
        # get the best mixtape based on mix score
        best_mixtape = max(complete_mixtapes, key= lambda tup: tup[3])
        # generate the mix script for the best mixtape
        return self.generate_simple_transition_script(best_mixtape[2])
    
    def generate_mix_path(self, start: MixGoal, end: MixGoal, tracks: int) -> List[Mix]:
        """
        Returns the optimal mix list between two goals for a given number of tracks.
        """
        raise NotImplementedError()

    
    def generate_simple_transition_script(self, mix_list: List[Mix]) -> List[Dict]:
        """
        Takes a list of Mix instances and generates the a Transition script using the simple Transition
        for each Mix.
        """
        transition_script = list()
        # get the first mix
        curr_mix = None
        # while there are still mixes in the mix_list
        while(len(mix_list) > 0):
            curr_mix = mix_list.pop(0)
            # create the transition
            curr_transition = Transition(curr_mix, self.style)
            # simplify that ish mang.
            curr_transition.create_ideal_intro_transition()
            curr_script =  curr_transition.to_script()
            transition_script.append(curr_script)

        return transition_script
        """
        TODO:
        Guarantee: effects list and transition list are in the same order.
        effects_list = {UserSong: [effect_1, effect_2, ...]}
        effect: {start_offset: integer, end_offset: integer, type: effect_type}
        """

    @ staticmethod 
    def compare_song_to_goal(song: Song, goal: MixGoal) -> float:
        """
            Return a value <= 0.0 comparing a Song to the MixGoal based on qualitative features.
            Lower value means higher similarity.
        """
        score = 0.0
        if not numpy.isnan(song.get_analysis_feature(Feature.DANCEABILITY)):
            score += numpy.abs(song.get_analysis_feature(Feature.DANCEABILITY) - goal.dance) 
        if not numpy.isnan(song.get_analysis_feature(Feature.ENERGY)):
            score += numpy.abs(song.get_analysis_feature(Feature.ENERGY) - goal.energy) 
        if not numpy.isnan(song.get_analysis_feature(Feature.VALENCE)):
            score += numpy.abs(song.get_analysis_feature(Feature.VALENCE) - goal.valence) 
        return score

    @staticmethod
    def mix_songs(a: usersong.UserSong, b: usersong.UserSong) -> Mix:
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
    def in_threshold_range(mix: Mix, min: numpy.array, max: numpy.array) -> bool:
        """
        Determines if mix is valid within threshold.

        Keyword args:
        """
        min_result = numpy.subtract(mix.threshold, min)
        # check all elements, if < 0 then return false
        assert isinstance(min_result, numpy.array)
        if numpy.any(min_result[:, 0] < 0):
            return False
        max_result = numpy.subtract(mix.threshold, max) 
        assert isinstance(max_result, numpy.array)
        if numpy.any(max_result[:, 0] > 0):
            return False
        # check all elements, if > 0 then return false
        return True

    @staticmethod
    def generate_3_track(a: Song, b: Song, c: Song) -> List[Dict]:
        """
        For testing purposes.
        Returns a structure ready for the composer that represents a mix between
        Song a --> Song b --> Song c using 16 beat crossfade/tempochange transition.
        """
        # get beat 16 beats from the end of Song a for transition 2
        beat_a_0 = len(a.get_analysis_feature(Feature.BEATS)) - 33
        # start beat 0 for Song b on transition 0
        beat_b_0 = 0
        # start beat 16 beats from end of Song b for transition 1
        beat_b_1 = len(b.get_analysis_feature(Feature.BEATS)) - 33
        # start beat 0 for Song c on transition 1
        beat_c_1 = 0
        # transition is length is always 16
        length = 32
        # pass transition type
        t_1 = Transition_Types.CROSSFADE
        t_2 = Transition_Types.TEMPO_MATCH
        mix = [
                {"song_a": a, "song_b": b, "start_a": beat_a_0,"start_b": beat_b_0, "sections":
                    [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                },
                {"song_a": b, "song_b": c, "start_a": beat_b_1, "start_b": beat_c_1, "sections":
                    [{"offset": 0, "length": length, "type": [t_1, t_2]}]
                }
            ]
        return mix