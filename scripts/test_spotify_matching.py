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
    sp_song = matcher.match_song(user_song)
    if sp_song is not None:
        matcher.merge_song_analysis(user_song, sp_song)
        print(user_song.get_analysis())
    else:
        print("No matching songs found")
#     user_song.analyze()
#     sp_songs = spotify.search_songs(user_song.get_name())
#     for sp_song in sp_songs:
#         sp_song.analyze()
#         print("Spotify song name: %s" % sp_song.get_name())
#         print("\tSpotify ID: %s" % sp_song.get_id())
#         print("\tSimilarity: %f\n" % song.similarity(user_song, sp_song))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("song", metavar="song", type=str, help="The song to match with Spotify")
    args = parser.parse_args()

    main(args)