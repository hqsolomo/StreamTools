import pick_audio

def test_pick_audio(path = "D:\\Users\\DAD\\Documents\\Repos\\StreamTools\\tests\\data\\short_audio"):
    assert pick_audio.pick_audio(path) != None

def test_valid_files(path = "D:\\Users\\DAD\\Documents\\Repos\\StreamTools\\tests\\data\\invalid_audio"):
    assert pick_audio.valid_files(path).__len__ == 1