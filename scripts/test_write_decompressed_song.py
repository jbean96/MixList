# pylint:disable=E1101
# pylint:disable=E0611
# PyLint can't resolve these warnings for some reason, so ignore them

import sys
import argparse

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import song

def main(args):
    s = song.Song(args.song)
    s.load()
    s.write_to_file()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test how a decompressed song file is written to a text file")
    parser.add_argument("song", metavar="song", help="The song to write to file")
    args = parser.parse_args()

    main(args)