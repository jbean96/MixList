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
    cut_samples = s.samples
    if args.cut_end is not None:
        sample_num = librosa.core.time_to_samples(args.cut_end, sr=s.sample_rate)
        if 0 < sample_num and sample_num < len(cut_samples):
            cut_samples = cut_samples[:sample_num]
    if args.cut_start is not None:
        sample_num = librosa.core.time_to_samples(args.cut_start, sr=s.sample_rate)
        if 0 < sample_num and sample_num < len(cut_samples):
            cut_samples = cut_samples[sample_num:]
    
    print("outputting to %s" % args.output)
    librosa.output.write_wav(args.output, y=cut_samples, sr=s.sample_rate)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test the time-stretch function by a given factor")
    parser.add_argument("song", metavar="song", type=str, help="The song to timestretch")
    parser.add_argument("--cut-start", "-cs", dest="cut_start", metavar="T", type=float, help="The time to do the start cut at")
    parser.add_argument("--cut-end", "-ce", dest="cut_end", metavar="T", type=float, help="The time to do the ending cut at")
    parser.add_argument("--output", "-o", dest="output", metavar="F", type=str, default="output.wav", help="Output file")
    args = parser.parse_args()

    main(args)