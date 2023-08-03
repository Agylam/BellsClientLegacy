import os
import re
import urllib.request
from dotenv import load_dotenv

from playsound import playsound
import websocket
import hashlib

 
load_dotenv()

SOUNDS_DIRNAME = "sounds"

API_SECRET = os.environ.get('API_SECRET')
SCHOOL_UUID = os.environ.get('SCHOOL_UUID')
ENDPOINT_URL = os.environ.get('ENDPOINT_URL')
SOUNDS_URL = os.environ.get('SOUNDS_URL')


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def get_filename(fullname):
    return re.search(r'^([a-f0-9\-]+)\.mp3$', fullname).group(1)


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



def on_open(ws):
    print("Соединение установлено")


def on_message(ws, message):
    print(f"Принятое сообщение: {message}")

    msg_splited = message.split(" ")
    cmd = msg_splited[0]
    args = msg_splited[1:]
    try:
        match cmd:
            case "PLAY":
                download_sound(args[0])
                print("Проигрывание файла",args[0])
                playsound(SOUNDS_DIRNAME+"/"+args[0]+".mp3", False)

            case "WARN":
                download_sound(args[0])

            case "AUTH_REQUEST":
                print("Отправляю аутентификационные данные")
                pred_hash = SCHOOL_UUID+API_SECRET+args[0]
                auth_cmd = "AUTH "+SCHOOL_UUID+" "+hashlib.sha256(pred_hash.encode()).hexdigest()
                ws.send(auth_cmd)
                print("Аутентификационные данные отправлены")

            case "AUTHORIZED":
                print("Успешная аутентификация!")

            case "ERROR":
                print("Ошибка от сервера:",' '.join(args))

            case _:
                print("Ошибка - неизвестная комманда от сервера")
    except Exception as e:
        print("Ошибка", e)

def on_close():
    print("Соединение закрыто")


ws = websocket.WebSocketApp(
    ENDPOINT_URL,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close,
)

ws.run_forever()

on_close()
