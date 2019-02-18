import argparse
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from analyzer.analyzer import usersong

def main(args):
    songs = usersong.load_songs(args.songs)
    for song in songs:
        print(song.get_analysis())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("songs", nargs="+", help="The songs to load")
    args = parser.parse_args()

    main(args)