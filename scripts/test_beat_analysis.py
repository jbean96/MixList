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

def main(args):
    song_paths = get_song_paths(args.directory)
    songs = list(map(song.Song, song_paths))[:(args.max if args.max is not None else len(song_paths))]
    for s in songs:
        s.load()

    for s in songs:
        print("Test beat analysis of: %s" % s.get_name())
        print("\ttempo: %f" % s.get_tempo())
        print("\tfirst beat: %f" % s.get_beats()[0])
        print()

def get_song_paths(directory, recursive=True):
    song_list = []
    with os.scandir(directory) as entry_iter:
        for entry in entry_iter:
            if entry.is_dir() and recursive:
                song_list.extend(get_song_paths(entry.path))
            elif entry.is_file():
                song_list.append(entry.path)
    
    return song_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check results from beat and tempo analysis")
    parser.add_argument("directory", metavar="dir", help="The directory to load songs from")
    parser.add_argument("--max", dest="max", metavar="N", type=int, help="Specify a maximum number of songs to load")
    args = parser.parse_args()
    
    main(args)