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

def squash_chroma_matrix(chroma_cq: np.ndarray, method: SquashMethod) -> np.ndarray:
    if method == SquashMethod.NORMALIZE:
        sum_rows = list(map(sum, chroma_cq))
        max_val = max(sum_rows)
        normalized_rows = list(map(lambda x: x / max_val, sum_rows))
        return normalized_rows
    elif method == SquashMethod.AVERAGE:
        return list(map(lambda x: sum(x) * 1.0 / len(x), chroma_cq))
    else:
        raise ValueError("No squash method defined for %s" % method)

def get_score(chroma_vector: np.ndarray, tone_profile: np.ndarray) -> float:
    if len(chroma_vector) != util.SEMITONES:
        raise ValueError("The length of the chroma vector is %d, should be %d" % (len(chroma_vector, util.SEMITONES)))
    if len(tone_profile) != util.SEMITONES:
        raise ValueError("The length of the tone profile vector is %d, should be %d" % (len(tone_profile, util.SEMITONES)))
    
    chroma_vector_length = np.sum(np.square(chroma_vector))
    tone_profile_length = np.sum(np.square(tone_profile))
    
    dot_product = np.dot(chroma_vector, tone_profile)

    return dot_product / (chroma_vector_length + tone_profile_length)

DEFAULT_SQUASH_METHOD = SquashMethod.NORMALIZE

def classify(samples: np.ndarray, sample_rate: int) -> keys.Camelot:
    chroma_cq = librosa.feature.chroma_cqt(y=samples, sr=sample_rate)
    squashed = squash_chroma_matrix(chroma_cq, DEFAULT_SQUASH_METHOD)
    scores = {}
    for mode in keys.Mode:
        for key in keys.Key:
            if key == keys.Key.NO_KEY:
                continue
            
            scores[(key, mode)] = get_score(squashed, tone_profiles.get_tone_profile(key, mode))
    
    max_key = max(scores.keys(), key=lambda x: scores[x])
    return keys.CAMELOT_KEYS[max_key]

def main(args: argparse.Namespace):
    samples, sr = librosa.load(args.file_path)
    print(classify(samples, sr))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get the key classification of a song")
    parser.add_argument("file_path", type=str, help="The file path to the song to analyze")
    args = parser.parse_args()
    main(args)
            