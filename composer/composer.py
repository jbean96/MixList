import os
import pipeclient

class composer(object):
    def __init__(self, song_list):
        self.client = pipeclient.PipeClient()
        self.songs = song_list

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

    def crossfade(self, leading_track_index, following_track_index, leading_track, following_track):
        # fade out out_track
        self.write("Select: Track=" + str(leading_track_index))
        #TODO: figure out why select time supports floats for end time but only int for start time
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
                dict['start_intro'] = 0
                dict['end_intro'] = dict['end_intro'] - shiftLeft
                dict['start_outro'] = dict['start_outro'] - shiftLeft
                dict['end_outro'] = dict['end_outro'] - shiftLeft

                # move cursor to the start of the next transition and store location
                self.write("SelectTime: Start=0, End=" + str(dict['start_outro']))
                self.write("SelSave: ")
            else:
                self.write("SelRestore: ")
                self.write("Align_StartToSelEnd: ")
                shiftRight = self.songs[i - 1]['start_outro'] - self.songs[i - 1]['start_intro']

                dict['start_intro'] = self.songs[i - 1]["start_outro"]
                dict['end_intro'] = dict['end_intro'] + shiftRight
                dict['start_outro'] = dict['start_outro'] + shiftRight
                dict['end_outro'] = dict['end_outro'] + shiftRight

                # move cursor to next position
                self.write("SelectTime: Start=0, End=" + str(dict["start_outro"]))
                self.write("SelSave: ")
            i = i + 1

    def trimsong(self, track, start_time, end_time):
        """
        trims everything outside of the start and end time
        """
        self.write("Select: Track=" + str(track))
        self.write("SelectTime: Start=" + str(start_time) + ", End=" + str(end_time))
        self.write("Trim: ")


def percent_change(startValue, endValue):
    return (float(endValue) / float(startValue) - 1) * 100
