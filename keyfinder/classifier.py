# pylint: disable=no-member
# pylint: disable=import-error

import argparse
import librosa
import numpy as np
import sys
from enum import auto, Enum

sys.path.append("..")

import util
import tone_profiles
from analyzer.analyzer import keys

class SquashMethod(Enum):
    NORMALIZE = auto()
    AVERAGE = auto()
    SUM = auto()

DEFAULT_SQUASH_METHOD = SquashMethod.SUM

def squash_chroma_matrix(chroma_cq: np.ndarray, method: SquashMethod) -> np.ndarray:
    if method == SquashMethod.NORMALIZE:
        sum_rows = np.sum(chroma_cq, axis=1)
        max_val = np.max(sum_rows)
        return np.apply_along_axis(lambda x: x / max_val, axis=0, arr=sum_rows)
    elif method == SquashMethod.AVERAGE:
        return np.apply_along_axis(lambda x: np.sum(x) / len(x), axis=1, arr=chroma_cq)
    elif method == SquashMethod.SUM:
        return np.sum(chroma_cq, axis=1)
    else:
        raise ValueError("No squash method defined for %s" % method)

def get_score(chroma_vector: np.ndarray, tone_profile: np.ndarray, octaves: int) -> float:
    if len(chroma_vector) != util.SEMITONES * octaves:
        raise ValueError("The length of the chroma vector is %d, should be %d" % (len(chroma_vector), util.SEMITONES * octaves))
    if len(tone_profile) != util.SEMITONES:
        raise ValueError("The length of the tone profile vector is %d, should be %d" % (len(tone_profile), util.SEMITONES))
    
    tone_profile_extended = np.array([])
    for i in range(octaves):
        tone_profile_extended = np.concatenate((tone_profile_extended, tone_profile * tone_profiles.OCTAVE_WEIGHTS[i]))
    assert len(chroma_vector) == len(tone_profile_extended) # sanity check
    chroma_vector_length = np.sqrt(chroma_vector.dot(chroma_vector))
    tone_profile_length = np.sqrt(tone_profile_extended.dot(tone_profile_extended))
    
    dot_product = np.dot(chroma_vector, tone_profile_extended)

    return dot_product / (chroma_vector_length * tone_profile_length)

# TODO: Change to be an option to collapse octaves or not instead of number of octaves..
def classify(samples: np.ndarray, sample_rate: int, octaves: int) -> keys.Camelot:
    if octaves <= 0 or octaves > util.OCTAVES:
        raise ValueError("Octaves must be > 0 and <= %d, you provided: %d" % (util.OCTAVES, octaves))
    if sample_rate <= 0:
        raise ValueError("Sample rate must be > 0, you provided: %d" % sample_rate)

    if octaves == 1:
        chroma_cq = librosa.feature.chroma_cqt(y=samples, sr=sample_rate)
    else: 
        chroma_cq = np.abs(librosa.core.cqt(y=samples, sr=sample_rate, n_bins=util.SEMITONES * octaves, bins_per_octave=util.SEMITONES))
    squashed = squash_chroma_matrix(chroma_cq, DEFAULT_SQUASH_METHOD)
    scores = {}
    for mode in keys.Mode:
        for key in keys.Key:
            if key == keys.Key.NO_KEY:
                continue
            
            scores[(key, mode)] = get_score(squashed, tone_profiles.get_tone_profile(key, mode), octaves)
    
    max_key = max(scores.keys(), key=lambda x: scores[x])
    return keys.CAMELOT_KEYS[max_key]

def main(args: argparse.Namespace):
    samples, sr = librosa.load(args.file_path)
    print(classify(samples, sr, 6))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the key classification of a song")
    parser.add_argument("file_path", type=str, help="The file path to the song to analyze")
    args = parser.parse_args()
    main(args)
            
