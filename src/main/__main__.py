import os
import time
import websocket
from dotenv import load_dotenv
load_dotenv()
from ws_events import on_close, on_message, on_open
from file_utils import init_folders

ENDPOINT_URL = os.environ.get('ENDPOINT_URL')


def execute_main():
    print("Текущая деректория:", os.getcwd())
    init_folders()

    while True:
        ws = websocket.WebSocketApp(
            ENDPOINT_URL,
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
        )
        ws.run_forever()
        on_close()
        print("Попытка повторного подключения...")
        time.sleep(1)

if __name__ == "__main__":
    execute_main()

