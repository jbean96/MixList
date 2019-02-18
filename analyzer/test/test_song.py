# pylint: disable=import-error
# pylint: disable=no-name-in-module

import sys

sys.path.append("..")

from analyzer import song
from analyzer import analysis

s1 = song.Song("Song1")
s1.set_analysis_feature(analysis.Feature.DURATION, 1000)
s1.set_analysis_feature(analysis.Feature.TEMPO, 128.0)

s2 = song.Song("Song2")
s2.set_analysis_feature(analysis.Feature.DURATION, 1000)
s2.set_analysis_feature(analysis.Feature.TEMPO, 128.0)

s3 = song.Song("Song3")
s3.set_analysis_feature(analysis.Feature.DURATION, 1200)
s3.set_analysis_feature(analysis.Feature.TEMPO, 140.0)

def test_get_analysis():
    s1_analysis = s1.get_analysis()
    assert s1_analysis.get_feature(analysis.Feature.TEMPO) == s1.get_analysis_feature(analysis.Feature.TEMPO)
    assert s1_analysis.get_feature(analysis.Feature.DURATION) == s1.get_analysis_feature(analysis.Feature.DURATION)

def test_similarity():
    assert song.similarity(s1, s2) == 1.0
    s2_s3 = song.similarity(s2, s3)
    assert s2_s3 < 1.0 and s2_s3 > 0.0
    s1_s3 = song.similarity(s1, s3)
    assert s1_s3 < 1.0 and s1_s3 > 0.0

def test_is_analyzed():
    assert s1.is_analyzed(analysis.Feature.DURATION) == True
    assert s1.is_analyzed(analysis.Feature.TEMPO) == True
    assert s1.is_analyzed(analysis.Feature.NAME) == True
    assert s1.is_analyzed(analysis.Feature.BEATS) == False
    assert s1.is_analyzed(analysis.Feature.VALENCE) == False