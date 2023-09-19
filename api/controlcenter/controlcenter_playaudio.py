from pydub import AudioSegment
from pydub.playback import play

#TODO: create one method to play a shortened clip
#TODO: create one method to play an entire clip
#TODO: create a method to play a clip on loop?
def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)