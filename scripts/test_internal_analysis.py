import argparse
import pickle
import sys

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from analyzer.analyzer import usersong

def main(args):
    s = usersong.UserSong(args.song)
    s.analyze()
    if args.output_path is None:
        print(s.get_analysis())
    else:
        with open(args.output_path, "wb") as out_file:
            out_file.write(pickle.dumps(s.get_analysis()))
            out_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test Spotify song matching")
    parser.add_argument("song", help="The song to internally analyze")
    parser.add_argument("--output", "-o", dest="output_path", type=str, metavar="path", help="The file to output the analysis to")
    args = parser.parse_args()

    main(args)