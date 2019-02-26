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
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTracks: Track=" + str(transition['following_track']) + " Mode=Add")
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.write("CrossfadeTracks: type=ConstantPower1 direction=OutIn")

    # TODO: make both fadein and fadeout transition agnostic (since only happens to one track)
    def fadein(self, transition):
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.write("Fade In:")

    def fadeout(self, transition):
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.write("Fade Out: ")

    def slidingstretch(self, RatePercentChangeStart, RatePercentChangeEnd):
        self.write("SlidingStretch: RatePercentChangeStart=" + str(RatePercentChangeStart) +
                   " RatePercentChangeEnd=" + str(RatePercentChangeEnd))

    def tempomatch(self, transition):
        """
        Script for tempo matching two tracks together. Must be called on each transition in reverse order
        """
        # Stretch following track
        self.write("Select: Track=" + str(transition['following_track']))
        self.write("SelectTime: Start=" + str(transition['following_start_transition']) + " End=" + str(transition['following_end_transition']))
        self.slidingstretch(percent_change(transition['following_tempo'], transition['leading_tempo']), 0)

        # Stretch leading track
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.slidingstretch(0, percent_change(transition["leading_tempo"], transition["following_tempo"]))

    def slidingstretchtest(self, startRate, endRate):
        self.write("Select: Track=0")
        self.write("SelectTime: Start=0 End=5.670")
        self.slidingstretch(startRate, endRate)

    def alignsongs(self):
        """
        for each song in songs[], trim the unused edges, then align each song
        """
        # First song in list has no intro transition and can be shift left if trimmed from the front
        song = self.songs[0]
        self.trimsong(0, song['start_intro'], song['end_outro'])
        # after trim, guaranteed to have song selected
        # first song in mix, align front and update values
        self.write("Align_StartToZero: ")
        shiftLeft = song['start_intro']
        song['start_intro'] = song['start_intro'] - shiftLeft
        song['end_intro'] = song['end_intro'] - shiftLeft
        song['start_outro'] = song['start_outro'] - shiftLeft
        song['end_outro'] = song['end_outro'] - shiftLeft

        # move cursor to the start of the next transition and store location
        self.write("SelectTime: Start=0 End=" + str(song['start_outro']))
        self.write("SelSave: ")

        i = 1
        offset = 0
        # Remainder of songs are trimmed and shifted right
        for song in self.songs[1:]:
            self.trimsong(i, song['start_intro'], song['end_outro'])
            # after trim, guaranteed to have song selected
            self.write("SelRestore: ")
            self.write("Align_StartToSelEnd: ")
            shiftRight = self.songs[i - 1]['start_outro'] - self.songs[i]['start_intro']
            offset = offset + shiftRight
            song['start_intro'] = self.songs[i - 1]["start_outro"]
            song['end_intro'] = song['end_intro'] + shiftRight
            song['start_outro'] = song['start_outro'] + shiftRight
            song['end_outro'] = song['end_outro'] + shiftRight

            # move cursor to next position
            self.write("SelectTime: Start=0 End=" + str(song["start_outro"]))
            self.write("SelSave: ")

            # Set transition times
            self.transitions[i - 1]['following_start_transition'] = song['start_intro']
            self.transitions[i - 1]['following_end_transition'] = song['end_intro']
            self.transitions[i - 1]['leading_start_transition'] = self.songs[i-1]['start_outro']
            self.transitions[i - 1]['leading_end_transition'] = self.songs[i-1]['end_outro']
            i = i + 1

    def trimsong(self, track, start_time, end_time):
        """
        trims everything outside of the start and end time
        """
        self.write("Select: Track=" + str(track))
        self.write("SelectTime: Start=" + str(start_time) + " End=" + str(end_time))
        self.write("Trim: ")

    def applytransitions(self):
        """
        Apply all transitions. Must be called last just before export()
        """
        for transition in self.transitions:
            for type in transition['types']:
                if type == 'none':
                    pass
                if type == 'crossfade':
                    self.crossfade(transition)

        # Last thing we do is loop through the songs stretching and merging in reverse order
        for transition in reversed(self.transitions):
            if 'tempomatch' in transition['types']:
                self.tempomatch(transition)
            # merge following track into leading track to preserve track alignment
            self.write("Select: Track=" + str(transition['leading_track']))
            self.write("SelectTracks: Track=" + str(transition['following_track']) + " Mode=Add")
            self.write("MixAndRender:")


class composer_parser(object):
    def __init__(self, transitions_array):
        self.transitions = transitions_array

    # TODO: handle multiple sections per transition
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
        beats_array = []
        while i < len(self.transitions):
            # Set Outro and tempo to leading song
            beats_array = self.transitions[i]['song_a'].get_analysis_feature(analysis.Feature.BEATS)
            c_songs[i]['start_outro'] = beats_array[self.transitions[i]['start_a']].get_start_time().item()
            c_songs[i]['end_outro'] = get_end_transition_timestamp(beats_array, self.transitions[i]['start_a'],
                                                          self.transitions[i]['sections'][0]['length'])

            # Set Intro to following song
            beats_array = self.transitions[i]['song_b'].get_analysis_feature(analysis.Feature.BEATS)
            start_time = beats_array[self.transitions[i]['start_b']].get_start_time()
            print("{}".format(start_time))
            c_songs.insert(i + 1, {
                'start_intro': start_time.item(),
                'end_intro': get_end_transition_timestamp(beats_array, self.transitions[i]['start_b'],
                                                          self.transitions[i]['sections'][0]['length']),
                'tempo': round(self.transitions[i]['song_b'].get_analysis_feature(analysis.Feature.TEMPO))

            })
            # Set transition
            c_transitions.insert(i, {
                'leading_track': i,
                'following_track': i+1,
                'leading_tempo': c_songs[i]['tempo'],
                'following_tempo': c_songs[i+1]['tempo'],
                'types': self.transitions[i]['sections'][0]['type']
            })
            i = i + 1

        last_index = len(c_songs) -1
        # Since last song does not have outro set to end of song
        c_songs[last_index]['start_outro'] = 0
        c_songs[last_index]['end_outro'] = beats_array[len(beats_array) - 1].get_start_time().item()

        # Start composer, Audacity must be running
        c = composer(c_songs, c_transitions)
        c.new()
        # The order of songs imported must match order of c_songs
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
