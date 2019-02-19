import argparse
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from analyzer.analyzer import usersong

def main(args):
    songs = usersong.load_songs_from_dir(args.directory)
    print("Loaded %d songs" % len(songs))
    for song in songs:
        print(song.get_name())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("directory", help="The directory to load songs from")
    args = parser.parse_args()

    main(args)