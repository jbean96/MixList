import librosa
from mixlist import song

class Analyzer:
    @staticmethod
    def analyze(song):
        # TODO: Appends analysis dictionary to the Song object
        pass

    def bpm(song):
        return librosa.beat.tempo(song.samples, sr=song.sample_rate)