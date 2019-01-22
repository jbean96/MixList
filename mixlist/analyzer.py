import librosa
from mixlist import song

class Analyzer:
    @staticmethod
    def analyze(song):
        song.analysis = {}
        song.analysis["bpm"] = Analyzer.bpm(song)

    @staticmethod
    def bpm(song):
        # TODO: Potentially use onset_envelope (need to lookup first)
        return librosa.beat.tempo(song.samples, sr=song.sample_rate)