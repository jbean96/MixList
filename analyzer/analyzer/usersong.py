# pylint: disable=no-name-in-module

import fnmatch
import librosa
import numpy as np
import os
import eyed3
from multiprocessing import Pool
from typing import List, Dict, Tuple
from tqdm import tqdm

from . import analysis
from . import matcher
from . import util
from .song import Song
from .keys import Camelot

class UserSong(Song):
    RESAMPLE_METHOD = 'kaiser_best' # ['kaiser_best', 'kaiser_fast', 'scipy']
    EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a'] # can add more if needed

    def __init__(self, path: str, load_on_init: bool=util.LOAD_SONGS_ON_INIT):
        self._path = os.path.abspath(path) # full file path to song on computer
        name = os.path.basename(self._path) # name with extension
        extension = name[name.rfind('.'):]
        name = name[:name.rfind('.')]
        if extension not in UserSong.EXTENSIONS:
            raise ValueError('File must be one of: %s' % UserSong.EXTENSIONS)
        self._extension = extension
        # If the extension is an mp3, load the id3 tag
        self._id3 = None
        try:
            self._id3 = eyed3.load(path).tag 
        except:
            pass

        super(UserSong, self).__init__(name)

        # Used to cache the rms arrays computed for the beats
        self._rms_frames = {}

        self._samples = None
        if load_on_init:
            self.load()
    
    def load(self):
        if self._samples is None:
            # print("Loading song %s" % self.get_name())
            self._samples = librosa.load(self._path, sr=util.SAMPLE_RATE, res_type=UserSong.RESAMPLE_METHOD)[0]

    def analyze(self):
        """
        Analyzes this song using internal analysis methods
        """
        if self._samples is None:
            raise ValueError('Song must be loaded before analysis')
            
        if self.is_analyzed(analysis.Feature.TEMPO) and \
            self.is_analyzed(analysis.Feature.BEATS) and \
                self.is_analyzed(analysis.Feature.DURATION):
            return 

        # Pre-matching analysis
        tempo, beats = analysis.analyze_beats(self._samples, util.SAMPLE_RATE)
        self.set_analysis_feature(analysis.Feature.TEMPO, tempo)
        self.set_analysis_feature(analysis.Feature.BEATS, analysis.annotate_downbeats(beats, util.DEFAULT_TIME_SIGNATURE))
        duration = analysis.analyze_duration(self._samples, util.SAMPLE_RATE)
        self.set_analysis_feature(analysis.Feature.DURATION, duration)
        self._is_internally_analyzed = True
        # song.set_analysis_feature(Analysis.Feature.KEY, Analyzer._analyze_key(song))

    def analyze_spotify(self) -> bool:
        """
        Gets the closest matching song from the Spotify API and merges it into this song's
        analysis, if there is no matching Spotify song, the UserSong is unchanged

        @return: A bool indicating whether or not a Spotify match was found
        """
        try:
            sp_song = matcher.match_song(self)
        except:
            return
        if sp_song is not None:
            matcher.merge_song_analysis(self, sp_song[0])
        else:
            return False # No spotify match found...

        time_signature = self.get_analysis_feature(analysis.Feature.TIME_SIGNATURE)
        # Only if we get a non 4 beats per measure time signature do we re-annotate the beats
        if time_signature is not None and time_signature > 0 and time_signature != 4:
            beats = self.get_analysis_feature(analysis.Feature.BEATS)
            self.set_analysis_feature(analysis.Feature.BEATS, analysis.annotate_downbeats(beats, time_signature))
        return True # Spotify match found!

    def get_amplitude_at_beat(self, beat: analysis.Beat, window_size: int) -> float:
        """
        Gets the average amplitude over a window at a beat

        @param beat: The beat to get the average amplitude at
        @param window_size: The half size of the window (must be a power of 2)
        """
        if window_size <= 0 or window_size > 4096:
            raise ValueError("Parameter window_size must be > 0")  
        if (window_size & (window_size - 1)) != 0:
            raise ValueError("Parameter window size must be a power of 2")
        if window_size in self._rms_frames:
            rms_array = self._rms_frames[window_size]
        else:
            self.load() # checks if there's no samples first
            rms_array = librosa.feature.rms(y=self._samples, frame_length=window_size*2, \
                center=True, hop_length=util.HOP_LENGTH)[0]
            self._rms_frames[window_size] = rms_array
        frame_index = beat.get_frame()
        if frame_index < 0 or frame_index >= len(rms_array):
            raise ValueError("Frame index is out of bounds")
        return rms_array[frame_index]

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

    def get_asys_file_name(self):
        return self.get_name() + ".asys"

    ### ONLY USED FOR TESTING ###
    def _set_samples(self, samples: np.ndarray):
        self._samples = samples

    def write_analysis_to_folder(self, folder_path: str):
        try:
            file_path = os.path.join(folder_path, self.get_asys_file_name())
            if not os.path.isfile(file_path):
                self.get_analysis().write_to_file(file_path)
        except:
            print("Error saving analysis to file: %s" % os.path.join(folder_path, self.get_asys_file_name()))

def analyze_user_song_from_cache(user_song: UserSong, cache_path: str) -> bool:
    if cache_path is not None:
        static_asys_path = os.path.join(cache_path, user_song.get_asys_file_name())
        if os.path.isfile(static_asys_path):
            try:
                user_song.set_analysis(analysis.from_file(static_asys_path))
                return True
            except:
                print("Error loading analysis from file: %s" % os.path.join(cache_path, static_asys_path))
    return False

def analyze_user_song(user_song: UserSong):
    user_song.load()
    user_song.analyze()
    if user_song.analyze_spotify():
        print("Found spotify match for %s" % user_song.get_name())

def batch_create_user_songs(file_paths: List[str], load_on_init: bool=util.LOAD_SONGS_ON_INIT) -> List[UserSong]:
    """
    Creates a List of unanalyzed user songs

    @param file_paths: A List of file paths to create UserSong objects from
    @param return: A List of UserSong objects (unanalyzed)
    """
    songs = list(map(lambda x: UserSong(x, load_on_init), file_paths))
    return songs

def batch_analyze_user_songs(user_songs: List[UserSong], cache_path: str=None):
    # TODO: Can we parallelize? Pool.map wasn't working...
    for i in tqdm(range(len(user_songs))):
        s = user_songs[i]
        if not analyze_user_song_from_cache(s, cache_path):
            analyze_user_song(s)

def load_songs_from_dir(directory: str, load_on_init: bool=util.LOAD_SONGS_ON_INIT) -> List[UserSong]:
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
    return batch_create_user_songs(file_paths, load_on_init)