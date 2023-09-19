# TODO: use files in working dir. need tamper protection to make sure it's our file
import json

CONFIG_PATH = r"D:\Users\DAD\Documents\Repos\StreamTools\config.json"
CONTENT_PATH = r"D:\Users\DAD\Documents\Repos\StreamTools\content.json"

def read_json_file(file_path):
    # TODO: input sanitization/validation prior to opening file
    with open(file_path, 'r') as f:
        return json.load(f)

config = read_json_file(CONFIG_PATH)
content = read_json_file(CONTENT_PATH)
