# pylint: disable=import-error
# pylint: disable=no-member

import numpy as np
import os
import sys

sys.path.append("..")
sys.path.append(os.path.join("..", ".."))

import tone_profiles
import util
from analyzer.analyzer import keys

def test_sum_profiles_equal():
    assert sum(tone_profiles.MAJOR_PROFILE) == sum(tone_profiles.MINOR_PROFILE)

def test_get_profile_basic():
    assert np.array_equal(tone_profiles.MAJOR_PROFILE, tone_profiles.get_tone_profile(keys.Key.C, keys.Mode.MAJOR))
    assert np.array_equal(tone_profiles.MINOR_PROFILE, tone_profiles.get_tone_profile(keys.Key.C, keys.Mode.MINOR))

def test_sharp_vs_flat():
    assert np.array_equal(tone_profiles.get_tone_profile(keys.Key.C_SHARP, keys.Mode.MAJOR),
        tone_profiles.get_tone_profile(keys.Key.D_FLAT, keys.Mode.MAJOR))
    assert np.array_equal(tone_profiles.get_tone_profile(keys.Key.F_SHARP, keys.Mode.MINOR),
        tone_profiles.get_tone_profile(keys.Key.G_FLAT, keys.Mode.MINOR))

def test_round_shift():
    d_major_tone_profile = tone_profiles.get_tone_profile(keys.Key.D, keys.Mode.MAJOR)
    assert np.array_equal(tone_profiles.MAJOR_PROFILE, tone_profiles.shift_tone_profile(d_major_tone_profile, 10))
    f_major_tone_profile = tone_profiles.get_tone_profile(keys.Key.F, keys.Mode.MAJOR)
    assert np.array_equal(tone_profiles.MAJOR_PROFILE, tone_profiles.shift_tone_profile(f_major_tone_profile, 7))
    g_sharp_minor_tone_profile = tone_profiles.get_tone_profile(keys.Key.G_SHARP, keys.Mode.MINOR)
    assert np.array_equal(tone_profiles.MINOR_PROFILE, tone_profiles.shift_tone_profile(g_sharp_minor_tone_profile, 4))
    b_minor_tone_profile = tone_profiles.get_tone_profile(keys.Key.B, keys.Mode.MINOR)
    assert np.array_equal(tone_profiles.MINOR_PROFILE, tone_profiles.shift_tone_profile(b_minor_tone_profile, 1))

def test_tone_profile_size():
    assert len(tone_profiles.MAJOR_PROFILE) == util.SEMITONES
    assert len(tone_profiles.MINOR_PROFILE) == util.SEMITONES

def test_octave_weights_size():
    assert len(tone_profiles.OCTAVE_WEIGHTS) == util.OCTAVES