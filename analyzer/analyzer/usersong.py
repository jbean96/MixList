# pylint: disable=no-name-in-module

import fnmatch
import librosa
import os
import eyed3
from multiprocessing import Pool
from typing import List, Dict, Tuple

from . import analysis
from . import matcher
from . import util
from .song import Song
from .keys import Camelot

class UserSong(Song):
    RESAMPLE_METHOD = 'kaiser_best' # ['kaiser_best', 'kaiser_fast', 'scipy']
    EXTENSIONS = ['.mp3', '.wav'] # can add more if needed

    def __init__(self, path: str, analyze_on_init: bool=False, load_static_analysis: bool=False):
        self._path = os.path.abspath(path) # full file path to song on computer
        name = os.path.basename(self._path) # name with extension
        extension = name[name.rfind('.'):]
        name = name[:name.rfind('.')]
        if extension not in UserSong.EXTENSIONS:
            raise ValueError('File must be one of: %s' % UserSong.EXTENSIONS)
        self._extension = extension
        # If the extension is an mp3, load the id3 tag
        self._id3 = eyed3.load(path).tag if extension == '.mp3' else None

        super(UserSong, self).__init__(name)

        self._samples = None

        analysis_loaded_from_file = False
        analysis_path = os.path.join(os.path.dirname(self._path), self.get_name() + ".asys")
        if load_static_analysis:
            try:
                if os.path.isfile(analysis_path):
                    asys = analysis.from_file(analysis_path)
                    self.set_analysis(asys)
                    analysis_loaded_from_file = True
            except:
                pass

        if not analysis_loaded_from_file:
            self._load()
            if analyze_on_init:
                self.analyze()
                self.analyze_spotify()
                self.get_analysis().write_to_file(analysis_path)
    
    def _load(self):
        self._samples = librosa.load(self._path, sr=util.SAMPLE_RATE, res_type=UserSong.RESAMPLE_METHOD)[0]

    def analyze(self):
        """
        Analyzes this song using internal analysis methods
        """
        if self._samples is None:
            raise ValueError('Song must be loaded before analysis')

        # Pre-matching analysis
        tempo, beats = analysis.analyze_beats(self._samples, util.SAMPLE_RATE)
        self.set_analysis_feature(analysis.Feature.TEMPO, tempo)
        self.set_analysis_feature(analysis.Feature.BEATS, analysis.annotate_downbeats(beats, util.DEFAULT_TIME_SIGNATURE))
        duration = analysis.analyze_duration(self._samples, util.SAMPLE_RATE)
        self.set_analysis_feature(analysis.Feature.DURATION, duration)
        # song.set_analysis_feature(Analysis.Feature.KEY, Analyzer._analyze_key(song))

    def analyze_spotify(self):
        """
        Gets the closest matching song from the Spotify API and merges it into this song's
        analysis, if there is no matching Spotify song, the UserSong is unchanged
        """
        sp_song = matcher.match_song(self)
        if sp_song is not None:
            matcher.merge_song_analysis(self, sp_song[0])
        else:
            return

        time_signature = self.get_analysis_feature(analysis.Feature.TIME_SIGNATURE)
        # Only if we get a non 4 beats per measure time signature do we re-annotate the beats
        if time_signature is not None and time_signature > 0 and time_signature != 4:
            beats = self.get_analysis_feature(analysis.Feature.BEATS)
            self.set_analysis_feature(analysis.Feature.BEATS, analysis.annotate_downbeats(beats, time_signature))

    def get_id3(self):
        """
        Returns the id3 tag of the song or None if it doesn't exist

        @return: This songs id3 tag
        """
        return self._id3

    def get_path(self):
        """
        Returns the file path to the song on the computer

        @return: The file path to the song
        """
        return self._path

    def get_extension(self):
        """
        Returns the extension of the song

        @return: The extension of the song
        """
        return self._extension

    def get_samples(self):
        """
        Return the samples of the song
        
        @return: np.ndarray of song samples
        """
        return self._samples

def create_analyzed_user_song(path: str) -> UserSong:
    return UserSong(path, True)

def load_songs(file_paths: List[str]) -> List[UserSong]:
    p = Pool(os.cpu_count())
    songs = p.map(create_analyzed_user_song, file_paths)
    return songs

def load_songs_from_dir(directory: str) -> List[UserSong]:
    if not os.path.isdir(directory):
        raise Exception("%s is not a directory" % directory)
    
    file_paths = []
    for root, _, files in os.walk(directory):
        for f in files:
            file_path = os.path.join(os.path.abspath(root), f)
            for ext in UserSong.EXTENSIONS:
                if fnmatch.fnmatch(file_path, "*%s" % ext):
                    file_paths.append(file_path)
                    break
    return load_songs(file_paths)