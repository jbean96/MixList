from typing import List, Dict, Any

from mixlist.analysis import Analysis
from mixlist import keys
from mixlist import util
from mixlist.song import Song

class SpotifySong(Song):
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

    def retrieve_analysis_data(self):
        """
        Retrieves the analysis data from the Spotify audio feature API and sets the features
        in the analysis object contained by this song
        """
        sp_features = util.sp.audio_features(self._id)[0]
        
        analysis_feature_map = {
            Analysis.Feature.DANCEABILITY : 'danceability',
            Analysis.Feature.ENERGY : 'energy',
            Analysis.Feature.KEY : ('key', 'mode'),
            Analysis.Feature.TEMPO : 'tempo',
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
        result = util.sp.search(q='track:%s' % song_name, type='track', limit=20)
        return list(map(lambda item: SpotifySong(item['artists'], item['name'], item['id']), result['tracks']['items']))