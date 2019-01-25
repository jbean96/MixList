import math
from mixlist import analyzer

class SongEditor:
    @staticmethod
    def volume_factor(song, factor):
        """
        Multiplies the samples of a song by a given factor

        :param song: The song to modify
        :param factor: The factor to multiply samples by
        """
        if factor == 1.0:
            return
        
        if not song.is_loaded():
            song.load()
        
        song.samples *= factor

    @staticmethod
    def insert_beat_clicks(song):
        """
        Inserts clicks at the analyzed beat times

        :param song: The song to insert beats in
        """
        if not song.is_loaded():
            song.load()
        
        if not song.is_analyzed(analyzer.Analyzer.AnalyzerEnums.BEATS):
            song.analyze(analyzer.Analyzer.AnalyzerEnums.BEATS)
        
        beats = song.analysis[analyzer.Analyzer.AnalyzerEnums.BEATS]
    
    @staticmethod
    def cut_song_end(song, time):
        """
        Cuts the song at the specified time leaving the samples from the start of the song to the cut time

        :param song: The song to modify
        :param factor: The time to cut at
        """
        song.samples, _ = SongEditor._cut_song(song, time)
    
    @staticmethod
    def cut_song_beginning(song, time):
        """
        Cuts the song at the specified time leaving the samples from the start of the song to the cut time

        :param song: The song to modify
        :param factor: The time to cut at
        """
        _, song.samples = SongEditor._cut_song(song, time)

    @staticmethod
    def _cut_song(song, time):
        if (time >= song.get_duration()):
            return (song.samples, song.samples)
        
        if not song.is_loaded():
            song.load()
        
        cut_index = math.floor(song.sample_rate * time)
        return (song.samples[:cut_index], song.samples[cut_index:])