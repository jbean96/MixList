import librosa
import os
from mixlist import analyzer

class Song:
    SAMPLE_RATE = 44100 # used as sample rate for all songs    
    RESAMPLE_METHOD = 'kaiser_best' # ['kaiser_best', 'kaiser_fast', 'scipy']

    def __init__(self, path):
        self._path = os.path.abspath(path)
        self._samples = None
        self._analysis = None
        
        self._load()
    
    def _load(self):
        print("Loading: %s" % self.get_name())
        self._samples = librosa.load(self.path, sr=Song.SAMPLE_RATE, res_type=Song.RESAMPLE_METHOD)[0]

    def _analyze(self):
        self._analysis = Analyzer.analyze(self)

    def get_samples(self):
        """
        Return the samples of the song
        
        @return: np.ndarray of song samples
        """
        return self._samples
    
    def get_name(self):
        """
        Return the basename of the song (i.e. without the entire path)

        @return: the basename of the song
        """
        return os.path.basename(self._path)

    def get_duration(self):
        """
        Gets the duration of the song

        @return: the duration of the song
        """
        return librosa.get_duration(self.samples, self.sample_rate)

    def 
