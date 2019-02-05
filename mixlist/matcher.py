from typing import List, Tuple

from . import spotify
from . import util
from . import song
from .usersong import UserSong

THRESHOLD = 0.9

@staticmethod
def match_song(user_song: UserSong) -> spotify.SpotifySong:
    pass

@staticmethod
def get_matching_songs(user_song: UserSong) -> List[spotify.SpotifySong]:
    """
    Gets the matching songs for a song from the Spotify API

    @param user_song: The song to query on the Spotify API
    @return: A list of matching SpotifySong objects, queried by name
    """
    sp_songs = spotify.search_songs(user_song.get_name())
    sp_features = util.sp.audio_features(tracks=map(lambda x: x.get_id(), sp_songs))
    map(lambda index, sp_song: sp_song.set_analysis_data(sp_features[index]))
    return sp_songs

@staticmethod
def score_matching_songs(user_song: UserSong, matches: List[spotify.SpotifySong]) -> List[Tuple(spotify.SpotifySong, float)]:
    if not user_song.is_analyzed():
        user_song.analyze()
    
    return map(lambda sp_song: (sp_song, song.similarity(user_song, sp_song)))

@staticmethod
def pick_closest_song(user_song: UserSong, sp_songs: List[spotify.SpotifySong], thresh=THRESHOLD) -> spotify.SpotifySong:
    scored_songs = score_matching_songs(user_song, sp_songs)
