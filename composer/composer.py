import os
import pipeclient

class composer(object):
    def __init__(self, instruction_dict):
        self.client = pipeclient.PipeClient()
        # Load instructions here? instruction_dict is the result of parsing json file
        self.instructions = instruction_dict

    def write(self, command):
        self.client.write(command)

    def read(self):
        """
        Returns response to last command
        """
        self.client.read()

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

    def crossfade(self, out_track, in_track, start_time, end_time):
        # fade out out_track
        self.write("Select: Track=" + out_track)
        self.write("SelectTime: Start=" + start_time + ", End=" + end_time)
        self.write("Fade Out: ")
        self.write("CursSelStart:")
        self.write("StoreCursorPosition:")

        # fade in in_track
        self.write("Select: Track=" + in_track)
        self.write("SelCursorStoredCursor")
        self.write("Align_StartToSelEnd:")
        self.write("SelectTime: Start=" + start_time + ", End=" + end_time)
        self.write("Fade In:")

    def tempomatch(self, out_track, in_track, start_time, end_time):
        return NotImplementedError()


def percent_change(startValue, endValue):
    return (startValue / endValue - 1) * 100

def main():
    """
    Using the instructions_dict, import the songs, apply transistions, export
    """
    return NotImplementedError
