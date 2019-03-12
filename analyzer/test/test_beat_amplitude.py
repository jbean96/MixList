import librosa

from analyzer import usersong
from analyzer import analysis

TEST_SONG = usersong.UserSong(librosa.util.example_audio_file(), False)
TEST_SONG.load()
TEST_SONG.analyze()

BEATS = TEST_SONG.get_analysis_feature(analysis.Feature.BEATS)

def test_errors():
    try:
        TEST_SONG.get_amplitude_at_beat(BEATS[0], 500)
        assert False
    except ValueError:
        assert True
    try:
        TEST_SONG.get_amplitude_at_beat(BEATS[0], -1)
        assert False
    except ValueError:
        assert True
    try:
        TEST_SONG.get_amplitude_at_beat(BEATS[0], 0)
        assert False
    except ValueError:
        assert True
    try:
        TEST_SONG.get_amplitude_at_beat(BEATS[0], 8192)
        assert False
    except ValueError:
        assert True
    
def test_valid_params():
    try:
        TEST_SONG.get_amplitude_at_beat(BEATS[0], 512)
        TEST_SONG.get_amplitude_at_beat(BEATS[len(BEATS)-1], 512)
        TEST_SONG.get_amplitude_at_beat(BEATS[0], 1024)
        TEST_SONG.get_amplitude_at_beat(BEATS[len(BEATS)-1], 1024)
        assert True
    except:
        assert False