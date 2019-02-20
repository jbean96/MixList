import argparse
import librosa
import os
import sys
from multiprocessing import Pool
from typing import Dict, List, Tuple

sys.path.append(os.path.join("..", ".."))

from analyzer.analyzer import keys
from keyfinder import classifier

def path_to_name(path: str) -> str:
    basename = os.path.basename(path)
    return basename[:basename.rfind('.')]

def collect_keys(directory: str) -> Dict[str, keys.Camelot]:
    key_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            name = path_to_name(f)
            with open(os.path.join(root, f), "r") as in_file:
                key_map[name] = keys.key_from_string(in_file.read())
                in_file.close()
    return key_map

def collect_audio_files(directory: str) -> Dict[str, str]:
    path_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            name = path_to_name(f)
            path_map[name] = os.path.join(root, f)
    return path_map

def get_test_tuples(args: argparse.Namespace) -> List[Tuple[str, keys.Camelot]]:
    key_map = collect_keys(args.annotations_dir)
    path_map = collect_audio_files(args.audio_dir)
    test_tuples = list(map(lambda x: (path_map[x], key_map[x]) if x in path_map else None, key_map.keys()))
    test_tuples = list(filter(lambda x: x is not None, test_tuples))
    return test_tuples

def compare_classifier_output(test_tuples: List[Tuple[str, keys.Camelot]]) -> Dict[keys.KeyRelationship, int]:
    counts = {}
    for relationship in keys.KeyRelationship:
        counts[relationship] = 0

    for tup in test_tuples:
        y, sr = librosa.load(tup[0])
        predicted_key = classifier.classify(y, sr)
        actual_key = tup[1]
        relationship = actual_key.get_relationship(predicted_key)
        counts[relationship] += 1
        print(relationship)
    return counts

def main(args: argparse.Namespace):
    test_tuples = get_test_tuples(args)
    p = Pool(os.cpu_count())
    results = p.map(compare_classifier_output, test_tuples[:10])
    #results = [compare_classifier_output(test_tuples[:10])]
    compiled_dict = {}
    for d in results:
        for key in d:
            if key not in compiled_dict:
                compiled_dict[key] = 0
            compiled_dict[key] += d[key]
    score = sum(map(lambda x: compiled_dict[x] * keys.KEY_RELATIONSHIP_SCORE[x], compiled_dict.keys()))
    total = sum(compiled_dict.values())
    if args.output:
        with open(args.output, "w") as out_file:
            out_file.write("EXACT,PERFECT_FOURTH,PERFECT_FIFTH,RELATIVE_KEY,PARALLEL_KEY,NONE,SCORE,TOTAL\n")
            out_file.write("%d,%d,%d,%d,%d,%d,%f,%d\n" % (compiled_dict[keys.KeyRelationship.EXACT],
                compiled_dict[keys.KeyRelationship.PERFECT_FOURTH], compiled_dict[keys.KeyRelationship.PERFECT_FIFTH],
                compiled_dict[keys.KeyRelationship.RELATIVE_KEY], compiled_dict[keys.KeyRelationship.PARALLEL_KEY],
                compiled_dict[keys.KeyRelationship.NONE], score, total))
            out_file.close()
    else:
        for key in compiled_dict:
            print("%s : %d" % (key, compiled_dict[key]))
        print("Score : %f" % score)
        print("Total : %d" % total)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test the key classifier against an annotated dataset")
    parser.add_argument("audio_dir", type=str, help="The directory containing the audio samples to test")
    parser.add_argument("annotations_dir", type=str, help="The directory containing the .KEY annotation files")
    parser.add_argument("--output", "-o", dest="output", metavar="F", type=str, help="The file to output to")

    args = parser.parse_args()
    main(args)