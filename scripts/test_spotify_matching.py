import argparse
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from analyzer.analyzer import spotify
from analyzer.analyzer import song
from analyzer.analyzer.usersong import UserSong
from analyzer.analyzer import matcher
from analyzer.analyzer import analysis

def main(args):
    user_song = UserSong(args.song)
    print("User song loaded...")
    print("Matching from Spotify.")
    sp_song = matcher.match_song(user_song)[0]
    if sp_song is not None:
        print("Found match!")
        matcher.merge_song_analysis(user_song, sp_song)
        print(sp_song.get_id())
        print(user_song.get_analysis_feature(analysis.Feature.KEY))
    else:
        print("No matching songs found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("song", metavar="song", type=str, help="The song to match with Spotify")
    args = parser.parse_args()

    main(args)