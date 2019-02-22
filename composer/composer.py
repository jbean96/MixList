import pipeclient
from analyzer.analyzer import analysis

class composer(object):
    def __init__(self, song_list, transition_list):
        self.client = pipeclient.PipeClient()
        self.songs = song_list
        self.transitions = transition_list

    def write(self, command):
        self.client.write(command)

    def read(self):
        """
        Returns response to last command
        """
        self.client.read()

    def new(self):
        self.write("New: ")

    def importaudio(self):
        """
        Opens Audacity import dialog box.
        User must navigate to playlist directory and select songs for import
        """
        self.write("ImportAudio:")

    def exportaudio(self):
        """
        Opens Audacity export dialog box.
        User must choose directory and name in which to save new audio file
        """
        self.write("Export:")

    def crossfade(self, transition):
        # fade out out_track
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['start_transition']) + " End=" + str(transition['end_transition']))
        self.write("Fade Out: ")

        # fade in in_track
        self.write("Select: Track=" + str(transition['following_track']))
        self.write("SelectTime: Start=" + str(transition['start_transition']) + " End=" + str(transition['end_transition']))
        self.write("Fade In:")

    def slidingstretch(self, RatePercentChangeStart, RatePercentChangeEnd):
        self.write("SlidingStretch: RatePercentChangeStart=" + str(RatePercentChangeStart) +
                   ", RatePercentChangeEnd=" + str(RatePercentChangeEnd))

    def tempomatch(self, transition):
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['start_transition']) + " End=" + str(transition['end_transition']))
        self.slidingstretch(0, percent_change(transition["leading_tempo"], transition["ending_tempo"]))
        self.write("Select: Track=" + str(transition['following_track']))
        self.write("SelectTime: Start=" + str(transition['start_transition']) + " End=" + str(transition['end_transition']))
        self.slidingstretch(percent_change(transition['ending_tempo'], transition['leading_tempo']), 0)


    def alignsongs(self):
        """
        for each song in songs[], trim the unused edges, then align each song
        """
        i = 0
        for dict in self.songs:
            self.trimsong(i, dict['start_intro'], dict['end_outro'])
            # after trim, guaranteed to have song selected
            if i == 0:
                # first song in mix, align front and update values
                self.write("Align_StartToZero: ")
                shiftLeft = dict['start_intro']
                dict['start_intro'] = dict['start_intro'] - shiftLeft
                dict['end_intro'] = dict['end_intro'] - shiftLeft
                dict['start_outro'] = dict['start_outro'] - shiftLeft
                dict['end_outro'] = dict['end_outro'] - shiftLeft

                # move cursor to the start of the next transition and store location
                self.write("SelectTime: Start=0 End=" + str(dict['start_outro']))
                self.write("SelSave: ")
            else:
                self.write("SelRestore: ")
                self.write("Align_StartToSelEnd: ")
                shiftRight = self.songs[i - 1]['start_outro'] - self.songs[i]['start_intro']

                dict['start_intro'] = self.songs[i - 1]["start_outro"]
                dict['end_intro'] = dict['end_intro'] + shiftRight
                dict['start_outro'] = dict['start_outro'] + shiftRight
                dict['end_outro'] = dict['end_outro'] + shiftRight

                # move cursor to next position
                self.write("SelectTime: Start=0 End=" + str(dict["start_outro"]))
                self.write("SelSave: ")

                for
            i = i + 1

    def trimsong(self, track, start_time, end_time):
        """
        trims everything outside of the start and end time
        """
        self.write("Select: Track=" + str(track))
        self.write("SelectTime: Start=" + str(start_time) + " End=" + str(end_time))
        self.write("Trim: ")

    def applytransitions(self):
        for transition in self.transitions:
            for type in transition['types']:
                if type == 'none':
                    pass
                if type == 'crossfade':
                    self.crossfade(transition)
        for transition in self.transitions:
            self.crossfade(transition)

class composer_parser(object):
    def __init__(self, transitions_array):
        self.transitions = transitions_array

    def compose(self):

        if len(self.transitions) < 0:
            return -1
        c_songs = []
        c_transitions = []

        # Intro for first song set to time=0
        c_songs.insert(0, {
            'start_intro': 0,
            'end_intro': 0,
            'tempo': round(self.transitions[0]['song_a'].get_analysis_feature(analysis.Feature.TEMPO))

        })

        i = 0
        while i < len(self.transitions):
            # Set Outro and tempo to leading song
            beats_array = self.transitions[i]['song_a'].get_analysis_feature(analysis.Feature.BEATS)
            c_songs[i]['start_outro'] = beats_array[self.transitions[i]['sections']['start_a']].get_start_time().item()
            c_songs[i]['end_outro'] = get_end_transition_timestamp(beats_array, self.transitions[i]['sections']['start_a'],
                                                          self.transitions[i]['sections']['length'])

            # Set Intro to following song
            beats_array = self.transitions[i]['song_b'].get_analysis_feature(analysis.Feature.BEATS)
            start_time = beats_array[self.transitions[i]['sections']['start_b']].get_start_time()
            print("{}".format(start_time))
            c_songs.insert(i + 1, {
                'start_intro': start_time.item(),
                'end_intro': get_end_transition_timestamp(beats_array, self.transitions[i]['sections']['start_b'],
                                                          self.transitions[i]['sections']['length']),
                'tempo': round(self.transitions[i]['song_b'].get_analysis_feature(analysis.Feature.TEMPO))

            })
            # Set transition
            c_transitions.insert(i, {
                'leading_track': i,
                'following_track': i+1,
                'start_transition': c_songs[i]['start_outro'],
                'end_transition': c_songs[i+1]['end_intro'],
                'leading_tempo': c_songs[i]['tempo'],
                'ending_tempo': c_songs[i+1]['tempo'],
                'types': self.transitions[i]['sections']['type']
            })
            i = i + 1

        last_index = len(c_songs) -1
        # Since last song does not have outro set to end of song
        c_songs[last_index]['start_outro'] = 0
        c_songs[last_index]['end_outro'] = beats_array[len(beats_array) - 1].get_start_time().item()

        # Start composer, Audacity must be running
        c = composer(c_songs, c_transitions)
        c.new()
        # The order of songs imported must match to order the the self.song_analysis
        c.importaudio()
        c.alignsongs()
        c.applytransitions()
        c.exportaudio()

def percent_change(startValue, endValue):
    return (float(endValue) / float(startValue) - 1) * 100

def get_end_transition_timestamp(beats_array, starting_index, num_beats):
    """
    :param beats_array: array of beats
    :param starting_index: the start of the transition
    :param num_beats: number of beats in the transition
    :return: the timestamp of the ending
    """
    return beats_array[starting_index + num_beats].get_start_time()
