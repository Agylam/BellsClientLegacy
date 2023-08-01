import os
import re

from dotenv import load_dotenv
import websocket
import hashlib

 
load_dotenv()

SOUNDS_DIRNAME = "sounds"

API_SECRET = os.environ.get('API_SECRET')
SCHOOL_UUID = os.environ.get('SCHOOL_UUID')
ENDPOINT_URL = os.environ.get('ENDPOINT_URL')
SOUNDS_URL = os.environ.get('SOUNDS_URL')


def get_filename(fullname):
    return re.search(r'^([a-f0-9]{32})\.mp3$', fullname).group(1)


def get_sounds():
    return list(map(get_filename, os.listdir(SOUNDS_DIRNAME)))


def download_sound(uuid):
    print(uuid)     
    print(get_sounds())



def on_open(ws):
    print("Соединение установлено")


def on_message(ws, message):
    print(f"Принятое сообщение: {message}")

    msg_splited = message.split(" ")
    cmd = msg_splited[0]
    args = msg_splited[1:]

    match cmd:

        case "PLAY":
            print(args[0])
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
