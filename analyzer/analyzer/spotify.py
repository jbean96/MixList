import re
from typing import List, Dict, Any

from . import keys
from . import util
from .analysis import Feature
from .song import Song

QUERY_LIMIT = 20

class SpotifySong(Song):
    def __init__(self, track: str, artists: List[Dict[str, Any]], spid: str):
        """
        Constructs a new SpotifySong

        @param track: The name of the track
        @param artists: A List of Spotify artist dictionaries
        @param spid: The Spotify ID of this track
        @return: A new SpotifySong object
        """
        super(SpotifySong, self).__init__(track)
        self._artists = list(map(lambda artist: artist['name'], artists))
        self._id = spid

    def __str__(self):
        return "artists: %s,\ntitle: %s,\nid: %s" % (self._artists, self._track_name, self._id)
    
    def get_id(self) -> str:
        """
        @return: The Spotify ID for this song
        """
        return self._id

    def get_artists(self) -> List[str]:
        """
        @return: A List of artists associated with this Song
        """
        return self._artists

    def analyze(self):
        """
        Analyzes this song with the Spotify API and stores it in the Analysis associated with this Song
        """
        sp_features = self._fetch_analysis_data()
        if sp_features is not None:
            self.set_analysis_data(sp_features)

    def _fetch_analysis_data(self) -> Dict[str, Any]:
        """
        Fetches analysis data from the Spotify API

        @return: The Spotify AudioFeatures object
        """
        return util.sp.audio_features(self.get_id())[0]

    def set_analysis_data(self, sp_features: Dict[str, Any]):
        """
        Retrieves the analysis data from the Spotify audio feature API and sets the features
        in the analysis object contained by this song

        @param sp_features: The Spotify AudioFeatures object returned from the API
        """
        if sp_features is None:
            raise ValueError("sp_features is empty for song with id %s, name %s" % (self.get_id(), self.get_name()))

        analysis_feature_map = {
            Feature.DANCEABILITY : 'danceability',
            Feature.DURATION : 'duration_ms',
            Feature.ENERGY : 'energy',
            Feature.KEY : ('key', 'mode'),
            Feature.TEMPO : 'tempo',
            Feature.TIME_SIGNATURE : 'time_signature',
            Feature.LOUDNESS : 'loudness',
            Feature.VALENCE : 'valence'
        }

        for analysis_feature in analysis_feature_map:
            if analysis_feature == Feature.KEY:
                musical_key = analysis_feature_map[analysis_feature][0]
                mode = analysis_feature_map[analysis_feature][1]
                if musical_key in sp_features and mode in sp_features:
                    self.set_analysis_feature(analysis_feature, keys.spotify_to_camelot(sp_features[musical_key], sp_features[mode]))

            if analysis_feature_map[analysis_feature] in sp_features:
                self.set_analysis_feature(analysis_feature, sp_features[analysis_feature_map[analysis_feature]])

def search_songs(query: str, limit: int=QUERY_LIMIT) -> List[SpotifySong]:
    """
    Searches for the matching songs in the Spotify API and returns them as list of potential
    matches, searches just based on track name

    @param song_name: The name of the song to query in the API
    @param limit: The max number of songs to return (defaults to SpotifySong.QUERY_LIMIT)
    @return: A list of SpotifySong objects corresponding to the returned songs from the query
    """
    query = re.sub('[!@#$\']', '', query)
    result = util.sp.search(q=query, type='track', limit=limit)
    return list(map(lambda item: SpotifySong(item['name'], item['artists'], item['id']), result['tracks']['items']))