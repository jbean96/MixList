import eyed3.id3
from typing import List, Tuple

from . import spotify
from . import util
from . import song

# A threshold can be specified such that if the first returned song in the first NUM_SONGS songs
# has a similarity value > MAX_THRESHOLD it will be chosen as the matching song
MAX_THRESHOLD = 0.975
# A minimum threshold can be specified such that if no song has a similarity score greater than
# the minimum threshold we don't consider there to be a matching song in the Spotify API
MIN_THRESHOLD = 0.90
# Specifies how many of the first songs to check to see if they are above the threshold to
# automatically select that as the matching song, will otherwise use the max song similarity
NUM_SONGS = 3

def _construct_query_from_id3(id3_tag: eyed3.id3.tag.Tag) -> str:
    track_name = id3_tag.title
    artist = id3_tag.album_artist if id3_tag.album_artist is not None else id3_tag.artist
    if track_name is None:
        return None
    query = 'track:%s' % track_name
    if artist is not None:
        query += ' artist:%s' % artist
    return query

def _construct_query_from_name(name: str) -> str:
    query = 'track:%s' % name
    return query

def _get_matching_songs(user_song: song.Song, num_songs: int=spotify.QUERY_LIMIT) -> List[spotify.SpotifySong]:
    """
    Gets the matching songs for a song from the Spotify API

    @param user_song: The song to query on the Spotify API
    @param num_songs: The number of songs to query on the Spotify
    @return: A list of matching SpotifySong objects, queried by name
    """
    sp_songs = None
    if user_song.get_id3() is not None:
        query = _construct_query_from_id3(user_song.get_id3())
        if query is not None:
            sp_songs = spotify.search_songs(query, num_songs)
    if sp_songs is None or len(sp_songs) == 0:
        query = _construct_query_from_name(user_song.get_name())
        sp_songs = spotify.search_songs(query, num_songs)
    # Queries the Spotify API with a batch of the songs instead of len(sp_songs)
    # separate queries
    sp_features = util.sp.audio_features(tracks=map(lambda x: x.get_id(), sp_songs))
    def _lambda_func(sp_song, sp_feature):
        if sp_feature is not None:
            sp_song.set_analysis_data(sp_feature)
            return sp_song
        else:
            return None
    # Map the returned audio features back to the respective SpotifySong
    return list(filter(lambda x: x is not None, map(_lambda_func, sp_songs, sp_features)))

def _score_matching_songs(user_song: song.Song, 
    matches: List[spotify.SpotifySong]) -> List[Tuple[spotify.SpotifySong, float]]:
    """
    Scores a list of SpotifySong objects by calculating their similarity to the user loaded song

    @param user_song: The user loaded song to compare to
    @param matches: The songs that were returned as matches when the user song was queried to
        the Spotify API
    @return: A list of tuples with the SpotifySong as the 0 index and the similarity score between
        that song and user_song in the 1 index
    """
    # The user song must be analyzed to compare with the spotify songs
    # TODO: Broken right now because is_analyzed just looks to see if the analysis object is
    # there, if we change to assume that songs are always analyzed this won't be an issue
    # if not user_song.is_analyzed():
    #     user_song.analyze()
    user_song.analyze()
    
    return list(map(lambda sp_song: (sp_song, song.similarity(user_song, sp_song)), matches))

def _pick_closest_song(sp_songs: List[Tuple[spotify.SpotifySong, float]], 
    max_thresh: float, min_thresh: float, num_songs: int) -> Tuple[spotify.SpotifySong, float]:
    """
    Picks the "closest" song to the user loaded song from a list of scored SpotifySong objects

    @param sp_songs: A list of scored SpotifySongs which should be tuples with the SpotifySong
        in the 0 index and the similarity score in the 1 index
    @param max_thresh: The threshold to compare the first num_songs, returns the first one that 
        surpasses the threshold, the default is mixlist.matcher.MAX_THRESHOLD
    @param min_thresh: The minimum threshold, if no songs have a similarity score greater than
        this value then no song will be returned (i.e. None)
    @param num_songs: The number of songs to compare max_thresh to, default is 
        mixlist.matcher.NUM_SONGS
    @return: The first of num_songs songs in the list that has a similarity score greater 
        than max_thresh or the max similarity scoring song in the list, or None if no song has
        a greater similarity score than min_thresh
    @raise: ValueError if max_thresh <= min_thresh
    """
    if max_thresh <= min_thresh:
        raise ValueError("max_thresh must be > min_thresh")

    # Look at the first num_songs songs, if any have a similarity greater than the max_thresh
    # return that song; assume that the songs the users want to mix are the most popular and so
    # use the ones returned first
    for i in range(min(num_songs, len(sp_songs))):
        if sp_songs[i][1] > max_thresh:
            return sp_songs[i]
    
    # Otherwise get the song with the maximum similarity from the scored song list
    best_tup = max(sp_songs, key=lambda x: x[1])
    # If it's less than min_thresh then we don't consider it a match and return nothing
    if best_tup[1] <= min_thresh:
        return None

    return best_tup

def match_song(user_song: song.Song, max_thresh: float=MAX_THRESHOLD, 
    min_thresh: float=MIN_THRESHOLD, num_songs: int=NUM_SONGS, 
    query_limit: int=spotify.QUERY_LIMIT) -> Tuple[spotify.SpotifySong, float]:
    """
    Matches a provided user loaded song to a song from the Spotify library

    @param user_song: The song to matchf
    @param max_thresh: The similarity score considered "high enough" for one of the first
        num_songs songs returned from the Spotify API to be selected as the matching song
    @param min_thresh: The minimum similarity score that will consider a "matched" song,
        otherwise no songs will be returned, the default value is mixlist.matcher.MIN_THRESHOLD
    @param num_songs: The number of songs to compare to the max_thresh, default is 
        mixlist.matcher.NUM_SONGS
    @param query_limit: The max number of songs to return from the Spotify API, default is
        mixlist.spotify.QUERY_LIMIT
    @return: The best matching SpotifySong from the Spotify API for the user loaded song or
        None if there was no SpotifySong with a similarity score greater than min_thresh or 
        if Spotify didn't have any results that matched the query
    """
    if query_limit > 50 or query_limit <= 0:
        raise ValueError("Query limit must be between 0 (exclusive) and 50 (inclusive)")
    
    if max_thresh <= min_thresh:
        raise ValueError("Max threshold needs to be greater than the min threshold")

    sp_songs = _get_matching_songs(user_song, query_limit)
    if len(sp_songs) == 0:
        # No matching songs
        return None
    scored_songs = _score_matching_songs(user_song, sp_songs)
    return _pick_closest_song(scored_songs, max_thresh, min_thresh, num_songs)

def merge_song_analysis(dest_song: song.Song, other_song: song.Song):
    """
    Merges one song's missing analysis features into another, modifies the analysis object
    of the dest_song argument in place

    @param dest_song: The song to merge anlalysis features into
    @param other_song: The song to get missing analysis features from
    """
    unanalyzed_features = dest_song.get_analysis().get_unanalyzed_features()
    for uf in unanalyzed_features:
        other_feature_val = other_song.get_analysis_feature(uf)
        if other_feature_val is not None:
            dest_song.set_analysis_feature(uf, other_feature_val)