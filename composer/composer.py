import time
import pipeclient
from analyzer.analyzer import analysis
from audio_effect_types import Transition_Types

"""
This class opens a new pipe client with Audacity to perform Audacity commands via
the scripting langauage
Audacity Scripting language reference:
https://manual.audacityteam.org/man/scripting_reference.html
"""
class composer(object):
    def __init__(self, song_list, transition_list, filepaths):
        self.client = pipeclient.PipeClient()
        self.songs = song_list
        self.transitions = transition_list
        self.filepaths = filepaths

    def write(self, command):
        """
        writes the command to the open pipe
        """
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
        Imports files
        """
        for filepath in self.filepaths:
            self.write("Import2:Filename=" + '"' + filepath + '"')

    def exportaudio(self):
        """
        Opens Audacity export dialog box.
        User must choose directory and name in which to save new audio file
        """
        self.write("Export:")

    def crossfade(self, transition):
        """
        Perform a simple crossfade between the tracks in transition

        """
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTracks: Track=" + str(transition['following_track']) + " Mode=Add")
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.write("CrossfadeTracks: type=ConstantPower1 direction=OutIn")

    def fadein(self, start_time, end_time):
        """
        Performs a fadeIn from start_time to end_time on the selected track
        """
        self.write("SelectTime: Start=" + str(start_time) + " End=" + str(end_time))
        self.write("Fade In:")

    def fadeout(self, start_time, end_time):
        """
        perform fadeout from start_time to end_time on selected track
        """
        self.write("SelectTime: Start=" + str(start_time) + " End=" + str(end_time))
        self.write("Fade Out: ")

    def slidingstretch(self, RatePercentChangeStart, RatePercentChangeEnd):
        """
        Perform a sliding stretch at the current selection
        :param RatePercentChangeStart: percentage of tempo change that will occur at the start of the selection
        :param RatePercentChangeEnd: percentage of tempo change that will occur at the end of the selection
        """
        self.write("SlidingStretch: RatePercentChangeStart=" + str(RatePercentChangeStart) +
                   " RatePercentChangeEnd=" + str(RatePercentChangeEnd))

    def changetempo(self, start_tempo, end_tempo, start_time, end_time):
        """
        performs a simple tempo change of the selected track from start_time to end_time. No sliding stretch applied.
        Track must be selected prior to calling tempochange
        :param start_tempo: the tempo we are changing from
        :param end_tempo: the tempo we are changing to
        :param start_time: the beginning of the selection
        :param end_time: the end of the selection
        """
        self.write("SelectTime: Start=" + str(start_time) + " End=" + str(end_time))
        change = percent_change(start_tempo, end_tempo)
        self.write("ChangeTempo: Percentage=" + str(change))

    def tempomatch(self, transition):
        """
        Perform a tempo match across two tracks. Time strectches track
        Stretches both songs
        """
        leading_tempo = transition["leading_tempo"]
        following_tempo = transition["following_tempo"]
        print('leading_tempo = ' + str(leading_tempo))
        print('following_tempo = ' + str(following_tempo))
        leading_tempo, following_tempo = tempomultiple(leading_tempo, following_tempo)
        print('leading_tempo = ' + str(leading_tempo))
        print('following_tempo = ' + str(following_tempo))
        # Stretch following track
        self.write("Select: Track=" + str(transition['following_track']))
        self.write("SelectTime: Start=" + str(transition['following_start_transition']) + " End=" + str(transition['following_end_transition']))
        self.slidingstretch(percent_change(following_tempo, leading_tempo), 0)

        # Stretch leading track
        self.write("Select: Track=" + str(transition['leading_track']))
        self.write("SelectTime: Start=" + str(transition['leading_start_transition']) + " End=" + str(transition['leading_end_transition']))
        self.slidingstretch(0, percent_change(leading_tempo, following_tempo))

    def tempomatch2(self, transition):
        """
        Stretches the leading song into the following songs tempo.
        Following track does not stretch
        """
        leading_tempo = transition["leading_tempo"]
        following_tempo = transition["following_tempo"]
        print('leading_tempo = ' + str(leading_tempo))
        print('following_tempo = ' + str(following_tempo))
        leading_tempo, following_tempo = tempomultiple(leading_tempo, following_tempo)
        print('leading_tempo = ' + str(leading_tempo))
        print('following_tempo = ' + str(following_tempo))

        # Stretch leading track
        self.write("Select: Track=" + str(transition['leading_track']))
        self.changetempo(leading_tempo, following_tempo,
                         transition['leading_start_transition'],
                         transition['leading_end_transition'])

    def alignsongs(self):
        """
        for each song in songs[], trim the unused edges, then align each song
        """
        # TODO: Do we want to support changes to the beginning of first song of mix? Currently supporting trimming only
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

        # Set transition times
        self.transitions[0]['following_start_transition'] = song['start_intro']
        self.transitions[0]['following_end_transition'] = song['end_intro']

        song_i = 1
        # Remainder of songs are trimmed and shifted right
        for song in self.songs[1:]:
            self.trimsong(song_i, song['start_intro'], song['end_outro'])
            # after trim, guaranteed to have song selected
            self.write("SelRestore: ")
            self.write("Align_StartToSelEnd: ")
            shiftRight = self.songs[song_i - 1]['start_outro'] - self.songs[song_i]['start_intro']
            song['start_intro'] = self.songs[song_i - 1]["start_outro"]
            song['end_intro'] = song['end_intro'] + shiftRight
            song['start_outro'] = song['start_outro'] + shiftRight
            song['end_outro'] = song['end_outro'] + shiftRight

            # move cursor to next position
            self.write("SelectTime: Start=0 End=" + str(song["start_outro"]))
            self.write("SelSave: ")

            transition_i = song_i - 1
            # Set transition times
            self.transitions[transition_i]['following_start_transition'] = song['start_intro']
            self.transitions[transition_i]['following_end_transition'] = song['end_intro']
            self.transitions[transition_i]['leading_start_transition'] = self.songs[transition_i]['start_outro']
            self.transitions[transition_i]['leading_end_transition'] = self.songs[transition_i]['end_outro']
            song_i = song_i + 1

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
                if type == Transition_Types.NONE:
                    pass
                if type == Transition_Types.CROSSFADE:
                    self.crossfade(transition)

        # Last thing we do is loop through the songs stretching and merging in reverse order
        for transition in reversed(self.transitions):
            if Transition_Types.TEMPO_MATCH in transition['types']:
                self.tempomatch(transition)
            if Transition_Types.TEMPO_MATCH2 in transition['types']:
                self.tempomatch2(transition)
            # merge following track into leading track to preserve track alignment
            self.write("Select: Track=" + str(transition['leading_track']))
            self.write("SelectTracks: Track=" + str(transition['following_track']) + " Mode=Add")
            self.write("MixAndRender:")

    def applyeffects(self):
        """
        Apply effects to each track
        """
        return NotImplementedError


# TODO: Change filepath to song analysis_feature
class composer_parser(object):
    def __init__(self, transitions_array, filepaths):
        self.transitions = transitions_array
        self.filepaths = filepaths

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
        c = composer(c_songs, c_transitions, self.filepaths)
        # calling new just before import throws an error because the window can't load fast enough
        c.new()
        time.sleep(3)
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

def tempomultiple(leading_tempo, following_tempo):
    """44100
    When a tempo change is too drastic to match, change tempo to a multiple of the leading tempo
    :param leading_tempo: the starting tempo
    :param following_tempo: the tempo we are stretching to.
    :return: new leading and following tempo
    """
    if leading_tempo < following_tempo:
        if abs(following_tempo - leading_tempo) > abs(leading_tempo - following_tempo/2):
            leading_tempo = following_tempo/2
    elif leading_tempo > following_tempo:
        if abs(following_tempo - leading_tempo) > abs(leading_tempo / 2 - following_tempo):
            following_tempo = leading_tempo / 2
    return leading_tempo, following_tempo