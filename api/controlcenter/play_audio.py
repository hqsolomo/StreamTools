import sys
from playsound import playsound
#This will be phased out to use pydub instead
file_path = sys.argv[1]
playsound(file_path)