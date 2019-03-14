import argparse
import fnmatch
import os

from analyzer import usersong

def _main(args: argparse.Namespace):
    file_paths = []
    walk_tuples = os.walk(args.in_dir)
    num_sep = args.in_dir.count(os.path.sep)
    if not args.recursive:
        walk_tuples = list(filter(lambda x: x[0].count(os.path.sep) == num_sep, walk_tuples))
    for root, _, files in walk_tuples:
        for f in files:
            file_path = os.path.join(os.path.abspath(root), f)
            for ext in usersong.UserSong.EXTENSIONS:
                if fnmatch.fnmatch(file_path, "*%s" % ext):
                    file_paths.append(file_path)
                    break
    
    user_songs = usersong.batch_create_user_songs(file_paths, False)
    for us in user_songs:
        if not args.force:
            if usersong.analyze_user_song_from_cache(us, args.out_dir):
                print("Found analysis %s for song %s" % (us.get_asys_file_name(), us.get_name()))
                continue
        usersong.analyze_user_song(us)
        print("Writing analysis for %s to %s" % (us.get_name(), os.path.join(args.out_dir, us.get_asys_file_name())))
        us.write_analysis_to_folder(args.out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a directory of songs and write their analyses to a directory")
    parser.add_argument("in_dir", help="The directory containing songs to analyze")
    parser.add_argument("out_dir", help="The directory to write song analyses to")
    parser.add_argument("-r", dest="recursive", action="store_true", help="Recursively look for songs in provided directory")
    parser.add_argument("-f", dest="force", action="store_true", help="Force analysis of previously analyzed songs")

    parser.set_defaults(recursive=False)
    parser.set_defaults(force=False)

    args = parser.parse_args()
    if not os.path.isdir(args.in_dir):
        raise Exception("Argument \"in_dir\" must be a directory")
    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    _main(args)