from typing import List, Tuple

from . import spotify
from . import util
from . import song
from .usersong import UserSong

# A threshold can be specified such that if the first returned song in the first NUM_SONGS songs
# has a similarity value > MAX_THRESHOLD it will be chosen as the matching song
MAX_THRESHOLD = 0.9
# A minimum threshold can be specified such that if no song has a similarity score greater than
# the minimum threshold we don't consider there to be a matching song in the Spotify API
MIN_THRESHOLD = 0.5
# Specifies how many of the first songs to check to see if they are above the threshold to
# automatically select that as the matching song, will otherwise use the max song similarity
NUM_SONGS = 3


def _get_matching_songs(user_song: UserSong) -> List[spotify.SpotifySong]:
    """
    Gets the matching songs for a song from the Spotify API

    @param user_song: The song to query on the Spotify API
    @return: A list of matching SpotifySong objects, queried by name
    """
    sp_songs = spotify.search_songs(user_song.get_name())
    # Queries the Spotify API with a batch of the songs instead of len(sp_songs)
    # separate queries
    sp_features = util.sp.audio_features(tracks=map(lambda x: x.get_id(), sp_songs))
    # Map the returned audio features back to the respective SpotifySong
    map(lambda index, sp_song: sp_song.set_analysis_data(sp_features[index]))
    return sp_songs

def _score_matching_songs(user_song: UserSong, 
    matches: List[spotify.SpotifySong]) -> List[Tuple(spotify.SpotifySong, float)]:
    """
    Scores a list of SpotifySong objects by calculating their similarity to the user loaded song

    @param user_song:
    @param matches:
    @return:
    """
    if not user_song.is_analyzed():
        user_song.analyze()
    
    return list(map(lambda sp_song: (sp_song, song.similarity(user_song, sp_song))))

def _pick_closest_song(user_song: UserSong, sp_songs: List[Tuple(spotify.SpotifySong, float)], 
    thresh: float, num_songs: int) -> spotify.SpotifySong:
    """
    Picks the "closest" song to the user loaded song from a list of scored SpotifySong objects

    @param user_song: The user loaded song to compare to
    @param sp_songs: A list of scored SpotifySongs which should be tuples with the SpotifySong
        in the 0 index and the similarity score in the 1 index
    @param thresh: The threshold to compare the first num_songs, returns the first one that 
        surpasses the threshold, the default is mixlist.matcher.MAX_THRESHOLD
    @param num_songs: The number of songs to compare thresh to, default is 
        mixlist.matcher.NUM_SONGS
    @return: The first of num_songs songs in the list that has a similarity score greater 
        than thresh or the max similarity scoring song in the list
    """
    for i in range(min(num_songs, len(sp_songs))):
        if sp_songs[i][1] > thresh:
            return sp_songs[i][0]
    
    return max(sp_songs, key=lambda x: x[1])[0]

def match_song(user_song: UserSong, thresh: float=MAX_THRESHOLD, num_songs: int=NUM_SONGS) -> spotify.SpotifySong:
    """
    Matches a provided user loaded song to a song in the 

    @param user_song:
    @param thresh:
    @param num_songs:
    @return:
    """
    sp_songs = _get_matching_songs(user_song)
    scored_songs = _score_matching_songs(user_song, sp_songs)
    return _pick_closest_song(user_song, scored_songs, thresh, num_songs)
