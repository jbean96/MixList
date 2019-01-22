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

def main(args):
    song_paths = get_song_paths(args.directory)
    songs = list(map(song.Song, song_paths))
    if (args.multi):
        songs = list(map(song.Song, song_paths))[:(args.max if args.max is not None else len(song_paths))]
        test_multi_process(songs)
    if (args.single):
        songs = list(map(song.Song, song_paths))[:(args.max if args.max is not None else len(song_paths))]
        test_single_process(songs)

def test_single_process(songs):
    timer = util.Timer()
    print("Single process loading of %d songs..." % len(songs))
    timer.start()
    for s in songs:
        s.load()
    timer.stop()

def test_multi_process(songs):
    timer = util.Timer()
    print("Multi process loading of %d songs..." % len(songs))
    timer.start()
    util.Methods.load_songs(songs)
    timer.stop()

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
    parser = argparse.ArgumentParser(description="Test single process vs. multi process song loading")
    parser.add_argument("directory", metavar="dir", help="The directory to load songs from")
    parser.add_argument("--max", dest="max", metavar="N", type=int, help="Specify a maximum number of songs to load")
    parser.add_argument("--single", "-s", dest="single", action="store_const", const=True, default=False, help="Use this option if you only want to test single process loading of the songs")
    parser.add_argument("--multi", "-m", dest="multi", action="store_const", const=True, default=False, help="Use this option if you only want to test multi process loading of the songs")
    args = parser.parse_args()

    if not (args.multi or args.single):
        args.multi = args.single = True
    
    main(args)