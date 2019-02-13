import librosa
import os
from typing import List, Dict, Tuple

from . import analysis
from .song import Song
from .keys import Camelot

class UserSong(Song):
    SAMPLE_RATE = 44100 # used as sample rate for all songs    
    RESAMPLE_METHOD = 'kaiser_best' # ['kaiser_best', 'kaiser_fast', 'scipy']
    EXTENSIONS = ['.mp3', '.wav'] # can add more if needed

    def __init__(self, path: str, analyze_on_init: bool=False):
        self._path = os.path.abspath(path) # full file path to song on computer
        name = os.path.basename(self._path) # name with extension
        extension = name[name.rfind('.'):]
        if extension not in UserSong.EXTENSIONS:
            raise ValueError('File must be one of: %s' % UserSong.EXTENSIONS)
        
        name = name[:name.rfind('.')]
        super(UserSong, self).__init__(name)

        self._samples = None
        self._load()
        if analyze_on_init:
            self.analyze()
    
    def _load(self):
        self._samples = librosa.load(self._path, sr=UserSong.SAMPLE_RATE, res_type=UserSong.RESAMPLE_METHOD)[0]

    def analyze(self):
        """
        Analyzes this song using internal analysis methods
        """
        if self._samples is None:
            raise ValueError('Song must be loaded before analysis')

        tempo, beats = UserSong._analyze_beats(self)
        # PRE-MATCHING ANALYSIS
        self.set_analysis_feature(analysis.Feature.TEMPO, tempo)
        self.set_analysis_feature(analysis.Feature.BEATS, beats)
        self.set_analysis_feature(analysis.Feature.DURATION, UserSong._analyze_duration(self))
        # song.set_analysis_feature(Analysis.Feature.KEY, Analyzer._analyze_key(song))
        # TODO: MATCH WITH SPOTIFY SONG
        # TODO: MERGE ANALYSIS FEATURES WITH SPOTIFY SONG
        # song.set_analysis_feature(analysis.Feature.BEATS, analysis.annotate_downbeats(beats, TIME_SIGNATURE_FROM_SPOTIFY))

    @staticmethod
    def _annotate_downbeats(song: 'UserSong', time_signature: int):
        """

        """
        pass

    @staticmethod
    def _analyze_beats(song: 'UserSong') -> Tuple[float, List[analysis.Beat]]:
        """
        Analyzes the tempo and the beats of this song and returns them as a tuple

        @return: A Tuple of (tempo, beats)
        """
        tempo, beats = librosa.beat.beat_track(song.get_samples(), sr=UserSong.SAMPLE_RATE, units=analysis.Beat.INDEX_VALUE)
        # Before getting time signature from spotify song, we assume 
        beats = list(map(lambda x: analysis.Beat(x, False), beats))
        return (tempo, beats)

    @staticmethod
    def _analyze_duration(song: 'UserSong') -> float:
        """
        Returns the duration of the song in seconds

        @return: The duration of the song in milliseconds
        """
        duration = librosa.get_duration(song.get_samples(), UserSong.SAMPLE_RATE)
        return duration * 1000 # want milliseconds
    
    @staticmethod
    def _analyze_key(song: 'UserSong') -> Camelot:
        # TODO: Add our own analysis of key to compare to Spotify API for additional validation
        pass

    def get_path(self):
        """
        Returns the file path to the song on the computer

        @return: The file path to the song
        """
        return self._path

    def get_samples(self):
        """
        Return the samples of the song
        
        @return: np.ndarray of song samples
        """
        return self._samples