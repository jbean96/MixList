import argparse
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist.song import Song
from mixlist.usersong import UserSong
from mixlist.spotifysong import SpotifySong

def main(args):
    user_song = UserSong(args.song)
    user_song.analyze()
    sp_songs = SpotifySong.search_songs(user_song.get_name())
    for sp_song in sp_songs:
        sp_song.analyze()
        print("Spotify song name: %s" % sp_song.get_name())
        print("\tSpotify ID: %s" % sp_song.get_id())
        print("\tSimilarity: %f\n" % Song.similarity(user_song, sp_song))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("song", metavar="song", type=str, help="The song to match with Spotify")
    args = parser.parse_args()

    main(args)