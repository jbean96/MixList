import matplotlib.pyplot as plt
import librosa.display
from enum import Enum, auto
from mixlist import song
from mixlist import analyzer

class Plotter:
    class PlotterEnums(Enum):
        WAVEFORM = auto()
        BEATS = auto()

    def __init__(self, song):
        self.song = song
        self.plots = []
    
    def plot_waveform(self):
        self.plots.append(Plotter.PlotterEnums.WAVEFORM)

    def plot_beat_sample(self):
        self.plots.append(Plotter.PlotterEnums.BEATS)

    def _draw_waveform(self):
        if not self.song.is_loaded():
            self.song.load()
        
        print("Drawing waveform of song %s" % self.song.get_name())
        librosa.display.waveplot(self.song.samples, sr=self.song.sample_rate)
    
    def _draw_beat_sample(self):
        if not self.song.is_loaded():
            self.song.load()

        if not self.song.is_analyzed(analyzer.Analyzer.AnalyzerEnums.BEATS):
            self.song.analyze(analyzer.Analyzer.AnalyzerEnums.BEATS)
        
        print("Drawing beat sample for first 10 (or fewer) beats of song %s" % self.song.get_name())
        beats = self.song.analysis[analyzer.Analyzer.AnalyzerEnums.BEATS]
        librosa.display.waveplot(self.song.samples, sr=self.song.sample_rate)
        plt.vlines(beats, -1.2, 1.2, alpha=0.5, color="r", linestyle="--", label="Beats")
        plt.xlim(beats[0] - 1, beats[min(10, len(beats) - 1)] + 1)
        plt.ylim(-1.2, 1.2)
    
    def draw_plot(self):
        rows = len(self.plots)
        if rows == 0:
            return
        
        _switch = {
            Plotter.PlotterEnums.WAVEFORM : Plotter._draw_waveform,
            Plotter.PlotterEnums.BEATS : Plotter._draw_beat_sample
        }

        plt.figure(1)
        for i in range(len(self.plots)):
           plt.subplot(rows, 1, i + 1)
           _switch[self.plots[i]](self)
        
        plt.show()