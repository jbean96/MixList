from analyzer import matcher

def test_simple():
    assert "this is a song" == matcher._remove_song_version("this is a song (dirty)")
    assert "this is a song" == matcher._remove_song_version("this is a song (clean)")
    assert "this is a song" == matcher._remove_song_version("this is a song (intro)")

def test_uppercase():
    assert "this is a song" == matcher._remove_song_version("this is a song (DiRTY)")
    assert "this is a song" == matcher._remove_song_version("this is a song (CleaN)")
    assert "this is a song" == matcher._remove_song_version("this is a song (inTRO)")

def test_other_stuff_in_parantheses():
    assert "this is a song" == matcher._remove_song_version("this is a song (some dirty mix)")
    assert "this is a song" == matcher._remove_song_version("this is a song (clean mix)")
    assert "this is a song" == matcher._remove_song_version("this is a song (another intro)")