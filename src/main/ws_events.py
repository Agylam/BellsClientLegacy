import os
import hashlib
from sound_utils import download_sound, delete_sound
from playsound import playsound

SOUNDS_DIRNAME = os.environ.get('SOUNDS_DIRNAME')
API_SECRET = os.environ.get('API_SECRET')
SCHOOL_UUID = os.environ.get('SCHOOL_UUID')


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
                playsound(SOUNDS_DIRNAME+"/bells/"+args[0]+".mp3", False)

            case "WARN":
                download_sound(args[0])

            case "ANNOUNCEMENT":
                download_sound(args[0], "announcements")
                print("Проигрывание объявления",args[0])
                playsound(SOUNDS_DIRNAME+"/announcements/"+args[0]+".mp3", False)
                ws.send("PLAYED_ANNOUNCEMENT "+args[0])
                delete_sound(args[0], "announcements")

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

            case "OK":
                pass

            case _:
                print("Ошибка - неизвестная комманда от сервера")
    except Exception as e:
        print("Ошибка", e)


def on_open(ws):
    print("Соединение установлено")


def on_close():
    print("Соединение закрыто")
