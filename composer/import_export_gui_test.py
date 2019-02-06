import os
import pipeclient

# Mocked optimizer instructions parsed from JSON
track0 = {
        "name" : "110bpm_8bars",
        "fadeout_start_time" : "10",
        "fadeout_end_time" : "18"
        }

track1 = {
        "name" : "120bpm_8bars",
        "fadein_start_time" : "0",
        "fadein_end_time" : "8"
        }

# t0,t1 mark the start and end of crossfade in seconds
t0 = track0["fadeout_start_time"]
t1 = track0["fadeout_end_time"]

client = pipeclient.PipeClient()

# Import tracks via window prompt
client.write("New:")
client.write("ImportAudio:")

# fadeout the first track
client.write("Select: Track=0")
client.write("SelectTime: Start=" + t0 + ", End=" + t1)
client.write("Fade Out: ")
client.write("CursSelStart:")
client.write("StoreCursorPosition:")

# fadein the second track
client.write("Select: Track=1")
client.write("SelCursorStoredCursor")
client.write("Align_StartToSelEnd:")
client.write("SelectTime: Start=" + t0 + ", End=" + t1)
client.write("Fade In:")
# export the mix
client.write("Export:")
