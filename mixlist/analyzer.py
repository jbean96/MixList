import librosa
from enum import Enum, auto

from mixlist.usersong import UserSong
from mixlist.analysis import Analysis

class Analyzer:
    BEAT_VALUE = 'time' # ['frames', 'samples', 'time']

    @staticmethod
    def analyze(song: UserSong):
        """
        Analyze the provided song and store it in the analysis attribute of the Song object

        @param song: the UserSong to analyze
        """
        tempo, beats = Analyzer._analyze_beats(song)
        song.set_analysis_feature(Analysis.Feature.TEMPO, tempo)
        song.set_analysis_feature(Analysis.Feature.BEATS, beats)

    @staticmethod
    def _analyze_beats(song: UserSong):
        tempo, beats = librosa.beat.beat_track(song.get_samples(), sr=UserSong.SAMPLE_RATE, units=Analyzer.BEAT_VALUE)
        return (tempo, beats)
    
    @staticmethod
    def _analyze_key(song):
        # TODO: Add our own analysis of key to compare to Spotify API for additional validation
        pass