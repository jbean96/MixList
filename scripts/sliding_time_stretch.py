# pylint:disable=E1101
# pylint:disable=E0611
# PyLint can't resolve these warnings for some reason, so ignore them

import os
import sys
import argparse
import numpy as np
import math
import librosa

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import song
from mixlist import util

def main(args):
    s = song.Song(args.song)
    s.load()
    splits = 1000 # could be variable depending on the number of samples
    new_samples = np.array([])
    chunk_length = math.floor(len(s.samples) / splits)
    diff = args.ef - args.sf
    for i in range(splits):
        min_sample = chunk_length * i
        if i == splits - 1:
            max_sample = len(s.samples)
        else:
            max_sample = min_sample + chunk_length

        factor = args.sf + (diff * 1.0 / splits) * i
        print("Stretching samples %d through %d by factor %f" % (min_sample, max_sample, factor))
        stretched = librosa.effects.time_stretch(s.samples[min_sample:max_sample], args.sf + (diff * 1.0 / splits) * i)
        new_samples = np.concatenate((new_samples, stretched))
    
    librosa.output.write_wav(args.output, y=new_samples, sr=s.sample_rate)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test the time-stretch function by a given factor")
    parser.add_argument("song", metavar="song", type=str, help="The song to timestretch")
    parser.add_argument("--start-factor", "-sf", dest="sf", type=float, metavar="F", default=1.0, help="The speed factor to start at the beginning of the song")
    parser.add_argument("--end-factor", "-ef", dest="ef", type=float, metavar="F", default=1.0, help="The ending speed factor of the song")
    parser.add_argument("--output", "-o", dest="output", metavar="F", type=str, default="output.wav", help="Output file")
    args = parser.parse_args()

    main(args)