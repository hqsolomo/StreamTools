import os
import random

class Selected_File:
    def __init__(self, directory, name, path):
        self.directory = directory
        self.name = name
        self.path = path
def pick_audio(path, contents):
    directory = ''
    if path in contents:
        directory = contents[path]
    files = os.listdir(directory)
    audio_files = [file for file in files if file.endswith(".mp3") or file.endswith(".wav")]
    if audio_files:
        random_audio_file = random.choice(audio_files)
        selected_file = Selected_File(path, random_audio_file,os.path.join(directory,random_audio_file))
    return selected_file
