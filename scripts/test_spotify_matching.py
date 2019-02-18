import argparse
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import spotify
from mixlist import song
from mixlist.usersong import UserSong
from mixlist import matcher

def main(args):
    user_song = UserSong(args.song)
    print("User song loaded...")
    print("Matching from Spotify.")
    sp_song = matcher.match_song(user_song)
    if sp_song is not None:
        print("Found match!")
        matcher.merge_song_analysis(user_song, sp_song)
        print(user_song.get_analysis())
    else:
        print("No matching songs found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("song", metavar="song", type=str, help="The song to match with Spotify")
    args = parser.parse_args()

    main(args)