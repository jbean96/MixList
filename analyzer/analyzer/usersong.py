# pylint: disable=no-name-in-module

import fnmatch
import librosa
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
    EXTENSIONS = ['.mp3', '.wav'] # can add more if needed

    def __init__(self, path: str):
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
    
    def load(self):
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
    user_song.analyze_spotify()

def batch_create_user_songs(file_paths: List[str]) -> List[UserSong]:
    """
    Creates a List of unanalyzed user songs

    @param file_paths: A List of file paths to create UserSong objects from
    @param return: A List of UserSong objects (unanalyzed)
    """
    songs = list(map(UserSong, file_paths))
    return songs

def batch_analyze_user_songs(user_songs: List[UserSong], cache_path: str=None):
    # TODO: Can we parallelize? Pool.map wasn't working...
    for i in tqdm(range(len(user_songs))):
        s = user_songs[i]
        if not analyze_user_song_from_cache(s, cache_path):
            analyze_user_song(s)

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
    return batch_create_user_songs(file_paths)