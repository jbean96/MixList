import numpy as np
import sys

sys.path.append("..")

from analyzer.analyzer import keys
    
def shift_tone_profile(tone_profile: np.ndarray, shift: int) -> np.ndarray:
    return np.roll(tone_profile, shift)

# Tone profiles taken from libKeyFinder specifically the ones specified in https://github.com/ibsh/libKeyFinder/blob/master/constants.cpp

MAJOR_PROFILE = np.array([
    7.23900502618145225142,
    3.50351166725158691406,
    3.58445177536649417505,
    2.84511816478676315967,
    5.81898892118549859731,
    4.55865057415321039969,
    2.44778850545506543313,
    6.99473192146829525484,
    3.39106613673504853068,
    4.55614256655143456953,
    4.07392666663523606019,
    4.45932757378886890365
])

MINOR_PROFILE = np.array([
    7.00255045060284420089,
    3.14360279015996679775,
    4.35904319714962529275,
    5.40418120718934069657,
    3.67234420879306133756,
    4.08971184917797891956,
    3.90791435991553992579,
    6.19960288562316463867,
    3.63424625625277419871,
    2.87241191079875557435,
    5.35467999794542670600,
    3.83242038595048351013
])

def get_tone_profile(key: keys.Key, mode: keys.Mode):
    if key == keys.Key.NO_KEY:
        raise ValueError("Cannot get tone profile for %s" % key)
    
    if mode == keys.Mode.MAJOR:
        return shift_tone_profile(MAJOR_PROFILE, key.value)
    elif mode == keys.Mode.MINOR:
        return shift_tone_profile(MINOR_PROFILE, key.value)
    else:
        raise ValueError("%s is not defined" % mode)

OCTAVE_WEIGHTS = np.array([
    0.39997267549999998559,
    0.55634425248300645173,
    0.52496636345143543600,
    0.60847548384277727607,
    0.59898115679999996974,
    0.49072435317960994006
])