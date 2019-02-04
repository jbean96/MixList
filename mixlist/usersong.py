import librosa
import os

from mixlist.analyzer import Analyzer
from mixlist.song import Song

class UserSong(Song):
    SAMPLE_RATE = 44100 # used as sample rate for all songs    
    RESAMPLE_METHOD = 'kaiser_best' # ['kaiser_best', 'kaiser_fast', 'scipy']
    EXTENSIONS = ['.mp3', '.wav'] # can add more if needed

    def __init__(self, path):
        self._path = os.path.abspath(path) # full file path to song on computer
        name = os.path.basename(self._path) # name with extension
        extension = name[name.rfind('.'):]
        if extension not in UserSong.EXTENSIONS:
            raise ValueError('File must be one of: %s' % UserSong.EXTENSIONS)
        
        name = name[:name.rfind('.')]
        super(UserSong, self).__init__(name)

        self._samples = None
        self._load()
    
    def _load(self):
        self._samples = librosa.load(self._path, sr=UserSong.SAMPLE_RATE, res_type=UserSong.RESAMPLE_METHOD)[0]

    def _analyze(self):
        if self._samples is None:
            raise ValueError('Song must be loaded before analysis')
        Analyzer.analyze(self)

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

    def get_duration(self):
        """
        Gets the duration of the song

        @return: the duration of the song
        """
        return librosa.get_duration(self._samples, UserSong.SAMPLE_RATE)