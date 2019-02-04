from typing import List, Dict, Any

from .analysis import Analysis
from . import keys
from . import util
from .song import Song

class SpotifySong(Song):
    SEARCH_LIMIT = 20

    def __init__(self, track: str, artists: List[Dict[str, Any]], spid: str) -> 'SpotifySong':
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
        self._set_analysis_data(sp_features)

    def _fetch_analysis_data(self) -> Dict[str, Any]:
        """
        Fetches analysis data from the Spotify API

        @return: The Spotify AudioFeatures object
        """
        return util.sp.audio_features(self.get_id())[0]

    def _set_analysis_data(self, sp_features: Dict[str, Any]):
        """
        Retrieves the analysis data from the Spotify audio feature API and sets the features
        in the analysis object contained by this song

        @param sp_features: The Spotify AudioFeatures object returned from the API
        """
        analysis_feature_map = {
            Analysis.Feature.DANCEABILITY : 'danceability',
            Analysis.Feature.DURATION : 'duration_ms',
            Analysis.Feature.ENERGY : 'energy',
            Analysis.Feature.KEY : ('key', 'mode'),
            Analysis.Feature.TEMPO : 'tempo',
            Analysis.Feature.TIME_SIGNATURE : 'time_signature',
            Analysis.Feature.LOUDNESS : 'loudness',
            Analysis.Feature.VALENCE : 'valence'
        }

        for analysis_feature in analysis_feature_map:
            if analysis_feature == Analysis.Feature.KEY:
                musical_key = analysis_feature_map[analysis_feature][0]
                mode = analysis_feature_map[analysis_feature][1]
                self.set_analysis_feature(analysis_feature, keys.spotify_to_camelot(sp_features[musical_key], sp_features[mode]))
                continue

            self.set_analysis_feature(analysis_feature, sp_features[analysis_feature_map[analysis_feature]])
    
    @staticmethod
    def search_songs(song_name: str) -> List['SpotifySong']:
        result = util.sp.search(q='track:%s' % song_name, type='track', limit=SpotifySong.SEARCH_LIMIT)
        return list(map(lambda item: SpotifySong(item['name'], item['artists'], item['id']), result['tracks']['items']))