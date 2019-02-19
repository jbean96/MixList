import composer

from analyzer.analyzer import analysis

class compose(object):
    def __init__(self, transitions_array):
        self.transitions = transitions_array

    def compose(self):
        c_songs = []
        c_transitions = []
        i = 0
        c_index = 0
        while i < len(self.transitions):
            beats_array = self.transitions['song_a'].get_analysis_feature(analysis.Feature.BEATS)

            start_intro = 0
            end_intro = 0
            if i != 0:
                # only need to set intro for songs after the first.
                start_intro = beats_array[self.transitions['sections']['start_a']]
                end_intro = get_end_transition_timestamp(beats_array, self.transitions['sections']['start_a'], self.transitions['sections']['length'])
            start_outro = beats_array[self.transitions['sections']['start_b']]
            end_outro = get_end_transition_timestamp(beats_array, self.transitions['sections']['start_b'], self.transitions['sections']['length'])
            tempo = self.transitions['song_a'].get_analysis_feature(analysis.Feature.TEMPO)

            c_songs[i] = {
                'start_intro': start_intro,
                'end_intro': end_intro,
                'start_outro': start_outro,
                'end_outro': end_outro,
                'tempo': tempo
            }

            i = i + 1

            beats_array = self.transitions['song_b'].get_analysis_feature(analysis.Feature.BEATS)
            start_intro = beats_array[self.transitions['sections']['start_b']]
            end_intro = get_end_transition_timestamp(beats_array, self.transitions['sections']['start_b'],
                                                     self.transitions['sections']['length'])
            start_outro = beats_array[self.transitions['sections']['start_b']]
            end_outro = get_end_transition_timestamp(beats_array, self.transitions['sections']['start_b'],
                                                 self.transitions['sections']['length'])
            tempo = self.transitions['song_b'].get_analysis_feature(analysis.Feature.TEMPO)

            c_songs[i] = {
                'start_intro': start_intro,
                'end_intro': end_intro,
                'start_outro': start_outro,
                'end_outro': end_outro,
                'tempo': tempo
            }

            c_transitions[c_index] = {
                'leading_track': i-1,
                'following_track': i,
                'start_transition': c_songs[i-1]['start_outro'],
                'end_transition': c_songs[i-1]['end_outro'],
                'leading_tempo': c_songs[i-1]['tempo'],
                'ending_tempo': c_songs[i]['tempo'],
                'types': self.transitions['sections']['type']
            }

            i = i + 1
            c_index = c_index + 1

        # Start composer, Audacity must be running
        c = composer(c_songs)
        c.new()
        # The order of songs imported must match to order the the self.song_analysis
        c.importaudio()
        c.alignsongs()
        c.applytransitions()
        c.exportaudio()

def get_end_transition_timestamp(beats_array, starting_index, num_beats):
    """
    :param beats_array: array of beats
    :param starting_index: the start of the transition
    :param num_beats: number of beats in the transition
    :return: the timestamp of the ending
    """
    return beats_array[starting_index + num_beats].get_start_time()

