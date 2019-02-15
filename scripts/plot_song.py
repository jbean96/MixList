import sys
import argparse
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Since the mixlist package is in the directory above this one
sys.path.append("..")

from mixlist import analysis
from mixlist import song
from mixlist import usersong

def main(args):
    s = usersong.UserSong(args.song)
    s.analyze()
    frame_length = 2048
    hop_length = int(frame_length / 4)
    rms = librosa.feature.rmse(y=s.get_samples(), frame_length=frame_length, hop_length=hop_length, center=True, pad_mode='symmetric')
    max_rms = max(rms[0])
    max_sample = max(s.get_samples())
    rms = list(map(lambda x: x * (max_sample / max_rms), rms[0]))
    plt.figure()
    plt.plot(s.get_samples())
    #librosa.display.waveplot(s.get_samples(), sr=usersong.UserSong.SAMPLE_RATE, x_axis='time')
    plt.plot([i * hop_length for i in range(len(rms))], rms)
    for xc in s.get_analysis_feature(analysis.Feature.BEATS):
        plt.axvline(x=xc.index, color='r', linestyle='--')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot a song and it's attributes")
    parser.add_argument("song", metavar="song", help="The song to plot")
    args = parser.parse_args()

    main(args)