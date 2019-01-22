import matplotlib.pyplot as plt
import librosa.display
from enum import Enum, auto
from mixlist import song
from mixlist import analyzer

class Plotter():
    class PlotterEnums(Enum):
        WAVEFORM = auto()

    def __init__(self, song):
        self.song = song
        self.plots = []
    
    def plot_waveform(self):
        self.plots.append(Plotter.PlotterEnums.WAVEFORM)

    def _draw_waveform(self):
        if not self.song.is_loaded():
            self.song.load()
        
        print("Drawing waveform of song %s" % self.song.get_name())
        librosa.display.waveplot(self.song.samples, sr=self.song.sample_rate)
    
    def draw_plot(self):
        plt.figure(1)
        rows = len(self.plots)
        if rows == 0:
            return
        
        _switch = {
            Plotter.PlotterEnums.WAVEFORM : Plotter._draw_waveform
        }

        for i in range(len(self.plots)):
           plt.subplot(rows, 1, i + 1)
           _switch[self.plots[i]](self)
        
        plt.show()