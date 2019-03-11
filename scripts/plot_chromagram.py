import argparse
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append("..")

from keyfinder import util

def main(args: argparse.Namespace):
    y, sr = librosa.load(args.file_path)
    chroma_cq = np.abs(librosa.core.cqt(y=y, sr=sr, n_bins=util.SEMITONES * util.OCTAVES, bins_per_octave=util.SEMITONES))
    print(chroma_cq)
    print(chroma_cq.shape)
    plt.figure()
    librosa.display.specshow(chroma_cq, y_axis='cqt_note', x_axis='time')
    plt.title("Chroma_CQT")
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot the constant-Q chromagram for a song")
    parser.add_argument("file_path", type=str, help="The file path of the song to plot")
    args = parser.parse_args()
    main(args)