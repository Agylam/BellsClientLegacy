import os
import urllib.request
from file_utils import get_filename, listdir_nohidden


SOUNDS_DIRNAME = os.environ.get('SOUNDS_DIRNAME')
SOUNDS_URL = os.environ.get('SOUNDS_URL')


def get_sounds():
    return list(map(get_filename, listdir_nohidden(SOUNDS_DIRNAME)))


def download_sound(uuid):
    downloaded_sounds = get_sounds()
    if uuid in downloaded_sounds:
        print("Звук",uuid,"уже загружен")
        return
    print("Звук",uuid,"загружается...")
    urllib.request.urlretrieve(SOUNDS_URL+"/"+uuid+".mp3", SOUNDS_DIRNAME+"/"+uuid+".mp3")
    print("Звук",uuid,"успешно загружен")