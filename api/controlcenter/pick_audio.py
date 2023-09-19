import os
import random
import streamtools_settings as s
from typing import List, Optional, Dict

# Add logic to handle more file types: mp3, wav, ogg, flac, etc...
# Probably needs a call to ffmpeg or something
def pick_audio(path: str):
    try:
        files = valid_files(os.scandir(s.content[path]))
        return random.choice(files)
    except FileNotFoundError:
        return None

# Check filetype against supported list
def valid_files(dir):
    output = []
    for entry in dir:
        if entry.is_file(follow_symlinks=False):
            for extension in s.config['supported_audio_extensions']:
                if entry.path.endswith(extension):
                    output.append(entry)
    return output
