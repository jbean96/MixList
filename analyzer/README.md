# Analyzer Module

## Getting Started

To install this module simply go to the top level analyzer folder and run `pip install -e .`

## analyzer/analyzer

Contains all of the modules for the MixList Analyzer

### Main Usage

The main module that should be used externally is the `usersong.py` module. This Object represents a song loaded from the computer on the user's system and contains an implementation of `song.analyze()` that does analysis on the loaded samples from the song as well as a method `song.analyze_spotify()` that uses the Spotify API to find a best matching song and merge the analysis data. 

Once a song has been analyzed you'll need to used the [Analysis](#the-analysis-object) Object defined in `analysis.py` to get features of a Song.

Loading a single song and then analyzing it
```python
from analyzer.analyzer import usersong

# Need to provide the entire path to the song so that the samples can be loaded
file_path = "mysong.mp3"
# You create a new song just by passing the file path
song = usersong.UserSong(file_path)
# To do any audio processing you need to load the song
song.load()
# First we do the internal analysis on the track
song.analyze()
# Then get the spotify analysis which merges it into this songs analysis
song.analyze_spotify()
```

We can also load the analysis of a song from a file
```python
from analyzer.analyzer import usersong

file_path = "mysong.mp3"
# analysis_cache should be the path to where you store static analyses
analysis_cache = "analysis_cache_folder"
# Create a user song object but don't load or analyze it
song = usersong.UserSong(file_path)
# analyze_user_song_from_cache will return a boolean indicating whether or not the
# analysis was succesfully loaded
loaded_from_cache = usersong.analyze_user_song_from_cache(song, analysis_cache)
if not loaded_from_cache:
    song.load()
    song.analyze()
    song.analyze_spotify()
```

Getting analysis features
```python
from analyzer.analyzer import analysis

# Returns an array of beat objects
beats = song.get_analysis_feature(analysis.Feature.BEATS)
for beat in beats:
    if beat.is_downbeat:
        print("Beat starting @ sample %d is a downbeat" % beat.get_start_sample())
        print("Beat starting @ time %f is a downbeat" % beat.get_start_time())
```

### The Analysis Object

The analysis object is present in every Song object and is a map of `analysis.Feature`s to their values, you can get a feature from an analysis object by using `analysis_obj.get_feature(analysis.Feature.FEATURE)`

You can look in `analyzer\analyzer\analysis.py` to see all current `analysis.Feature`s, but here is a list with explanations of what the values are:

- Internally analyzed features:
    - analysis.Feature.BEATS
        - Contains a `List` of `analysis.Beat` Objects
            - an `analysis.Beat` Object has two fields: `index` and `is_downbeat`
                - `index` is the index of the beat which is either a timestamp or a sample number for the beginning of the beat
                - `is_downbeat` is a `boolean` indicating if the beat is a downbeat
                - Also has methods `get_start_time()` and `get_start_sample()` which will return the starting time/sample regardless of what the stored value is
    - analysis.Feature.DURATION
        - A `float` indicating the duration of the song in milliseconds
    - analysis.Feature.NAME
        - A `str` containing the song name
    - analysis.Feature.TEMPO
        - A `float` indicating the estimated tempo (in beats-per-minute) of the song
- Spotify features:
    - analysis.Feature.DANCEABILITY
        - A Spotify defined `float`
    - analysis.Feature.ENERGY
        - A Spotify defined `float`
    - analysis.Feature.KEY
        - A `Camelot` Object which you can find in `analyzer\analyzer\keys.py` indicating the Camelot key of the song or `None` if the key couldn't be detected
    - analysis.Feature.LOUDNESS
        - A Spotify defined `float`
    - analysis.Feature.TIME_SIGNATURE
        - An `int` indicating the time signature of the song, is used to help annotate the beats on whether or not they are a downbeat
    - analysis.Feature.VALENCE
        - A Spotify defined `float`

```python
from analyzer.analyzer import analysis

# Returns an array of beat objects
beats = song.get_analysis_feature(analysis.Feature.BEATS)
for beat in beats:
    if beat.is_downbeat:
        print("Beat starting @ sample %d is a downbeat" % beat.get_start_sample())
        print("Beat starting @ time %f is a downbeat" % beat.get_start_time())
```

If we've decided that we want to mix two objects `song1` and `song2` starting at a certain timestamp `t1` for `song1` and `t2` for `song2` then you can get the closest beat for those two songs with the following code
```python
from analyzer.analyzer import analysis

# by passing False as the third parameter, the algorithm will look for
# closest beat overall
song1_beat = analysis.get_closest_beat_to_time(beats, t1, False)
song2_beat = analysis.get_closest_beat_to_time(beats, t2, False)

# Then to get the corresponding time you can do:
song1_time = song1_beat.get_start_time()
song2_time = song2_beat.get_start_time()

# alternatively you can force it to find downbeats
song1_downbeat = analysis.get_closest_beat_to_time(beats, t1, True)
song2_downbeat = analysis.get_closest_beat_to_time(beats, t2, True)
```