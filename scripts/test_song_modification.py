# pylint:disable=E1101
# pylint:disable=E0611
# PyLint can't resolve these warnings for some reason, so ignore them

import os
import sys
import argparse

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import song
from mixlist import util
from mixlist import analyzer
from mixlist import songeditor

def main(args):
    s = song.Song(args.song)
    if args.volume is not None:
        songeditor.SongEditor.volume_factor(s, args.volume)
    if args.cut_begin is not None:
        songeditor.SongEditor.cut_song_beginning(s, args.cut_begin)
    if args.cut_end is not None:
        songeditor.SongEditor.cut_song_end(s, args.cut_end)

    s.output(args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check results from beat and tempo analysis")
    parser.add_argument("song", metavar="song", help="The directory to load songs from")
    parser.add_argument("--volume", "-v", dest="volume", metavar="F", type=float, help="The volume factor to multiply the song by")
    parser.add_argument("--output", "-o", dest="output", default="output.wav", metavar="file", type=str, help="The destination file to output the resulting song to, default is output.wav")
    parser.add_argument("--cut_end", "-ce", dest="cut_end", metavar="time", type=float, help="The time to end the song at")
    parser.add_argument("--cut_begin", "-cb", dest="cut_begin", metavar="time", type=float, help="The start the song at")

    args = parser.parse_args()
    
    main(args)