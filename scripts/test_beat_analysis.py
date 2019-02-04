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
    if args.dir is not None and os.path.isdir(args.dir):
        song_paths = get_song_paths(args.dir)
        songs = list(map(song.Song, song_paths))[:(args.max if args.max is not None else len(song_paths))]
    elif args.file is not None and os.path.isfile(args.file):
        songs = [song.Song(args.file)]
    else:
        print("Invalid file or directory")
        sys.exit(1)

    for s in songs:
        s.load()

    for s in songs:
        print("Test beat analysis of: %s" % s.get_name())
        print("\ttempo: %s" % s.get_tempo())
        print("\tfirst 10 beats: %s" % s.get_beats()[:10 if len(s.get_beats()) >= 10 else len(s.get_beats())])
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
    parser.add_argument("--dir", "-d", dest="dir", metavar="dir", help="Test multiple songs from a directory")
    parser.add_argument("--max", dest="max", metavar="N", type=int, help="Specify a maximum number of songs to load if loading from a directory")
    parser.add_argument("--file", "-f", dest="file", metavar="F", help="Test a single file")
    args = parser.parse_args()

    if args.dir is None and args.file is None:
        print("Must specify a directory with --dir or a file with --file")
        sys.exit(1)
    
    main(args)