import pipeclient

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
                if type == 'tempomatch':
                    self.tempomatch(transition)

def percent_change(startValue, endValue):
    return (float(endValue) / float(startValue) - 1) * 100
