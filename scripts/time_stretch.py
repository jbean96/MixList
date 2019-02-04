# pylint:disable=E1101
# pylint:disable=E0611
# PyLint can't resolve these warnings for some reason, so ignore them

import os
import sys
import argparse
import librosa

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import song
from mixlist import util

def main(args):
    s = song.Song(args.song)
    s.load()
    stretched = librosa.effects.time_stretch(s.samples, args.factor)
    librosa.output.write_wav(args.output, y=stretched, sr=s.sample_rate)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test the time-stretch function by a given factor")
    parser.add_argument("song", metavar="song", type=str, help="The song to timestretch")
    parser.add_argument("factor", metavar="factor", type=float, help="The factor to timestretch by")
    parser.add_argument("--output", "-o", metavar="F", type=str, default="output.wav", help="Output file")
    args = parser.parse_args()

    main(args)