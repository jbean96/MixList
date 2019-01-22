# pylint:disable=E1101
# pylint:disable=E0611
# PyLint can't resolve these warnings for some reason, so ignore them

import sys
import argparse

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import song
from mixlist import plotter

def main(args):
    p = plotter.Plotter(song.Song(args.song))
    if (args.wave):
        p.plot_waveform()
    p.draw_plot()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot a song and it's attributes")
    parser.add_argument("song", metavar="song", help="The song to plot")
    parser.add_argument("--wave", "-w", dest="wave", default=False, const=True, action="store_const", help="Plot the waveform of the song")
    args = parser.parse_args()

    main(args)