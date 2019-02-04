import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from enum import auto, Enum
from typing import Any, List, Dict

from mixlist import keys

# Setup with the spotipy library

CLIENT_ID = '3f1aa13bb7db466fa6294a27157b3776'
CLIENT_SECRET = '608ad2aef74c494795d6e0d7927de725'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Analysis:
    class Feature(Enum):
        DANCEABILITY = auto()
        ENERGY = auto()
        KEY = auto()
        TEMPO = auto()
        LOUDNESS = auto()
        VALENCE = auto()
        
    def __init__(self) -> 'Analysis':
        self._features = {}

    def __str__(self) -> str:
        return str(self._features)
    
    def set_feature(self, feature: Feature, value: Any):
        self._features[feature] = value

class SpotifySong:
    def __init__(self, artists: List[Dict[str, Any]], track: str, spid: str) -> 'SpotifySong':
        self._artists = list(map(lambda artist: artist['name'], artists))
        self._track_name = track
        self._id = spid
        self._analysis = Analysis()

    def __str__(self):
        return "artists: %s,\ntitle: %s,\nid: %s" % (self._artists, self._track_name, self._id)

    def set_analysis_feature(self, feature: Analysis.Feature, value: Any):
        self._analysis.set_feature(feature, value)

    def retrieve_feature_data(self):
        sp_features = sp.audio_features(self._id)[0]
        
        self.set_analysis_feature(Analysis.Feature.DANCEABILITY, sp_features['danceability'])
        self.set_analysis_feature(Analysis.Feature.ENERGY, sp_features['energy'])
        self.set_analysis_feature(Analysis.Feature.KEY, keys.spotify_to_camelot(sp_features['key'], sp_features['mode']))
        self.set_analysis_feature(Analysis.Feature.TEMPO, sp_features['tempo'])
        self.set_analysis_feature(Analysis.Feature.LOUDNESS, sp_features['loudness'])
        self.set_analysis_feature(Analysis.Feature.VALENCE, sp_features['valence'])
    
    def get_analysis(self) -> Analysis:
        return self._analysis

def search_songs(song_name):
    result = sp.search(q='track:%s' % song_name, type='track', limit=20)
    return list(map(lambda item: SpotifySong(item['artists'], item['name'], item['id']), result['tracks']['items']))

songs = search_songs('Boomerang')
for song in songs:
    song.retrieve_feature_data()
    print(song.get_analysis())