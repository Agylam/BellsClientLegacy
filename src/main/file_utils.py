import os
import re

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def get_filename(fullname):
    return re.search(r'^([a-f0-9\-]+)\.mp3$', fullname).group(1)

def init_folders():
    folders = ["sounds", "sounds/bells", "sounds/announcements"]
    for folder in folders:
        if not os.path.isdir(folder):
            os.mkdir(folder)
