##########################
## 서버

import asyncio
import websockets
import json
import time

print("open?")
async def app_opencv(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            print(message)
            if len(message) == 0 or message == "undefined":
                continue
            data = [json.loads(message)]

            time.sleep(1)
            data+='DEBUG'
            result_json = json.dumps(data)
            print(result_json)
            try:
                if websocket.open:
                    print("sended!")
                    await websocket.send(result_json)
            except Exception as e:
                print(f"send error: {str(e)}")

    except websockets.exceptions.ConnectionClosedOK:
        pass

start_server = websockets.serve(app_opencv, "localhost", 8085)  


async def main():
    await start_server


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()





################################################################
################################################################

## 클라
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController # 1인칭 컨트롤러
import websocket
import threading
import numpy as np

hand1 = np.zeros((21,3))
hand2 = np.zeros((21,3))


def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened!!!")
    # ws.send("Hello, server!") # 형식 xx

def run_ursina_app():
    app = Ursina()
    mouse.visible = False

    main_floor = Entity(model = 'cube', position=(0,0,0), scale=(45,1,50), color = color.gray, collider = 'box')

    # EditorCamera()
    player = FirstPersonController() # 조작: WASD, Space, mouse
    player.cursor.visible = False # 커서 없애기
    player.gravity = 0.5 # 중력
    player.speed = 15 # 속도 변경 (기본값 10?)

    app.run()



def websocket_thread():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8085/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    websocket_thread = threading.Thread(target=websocket_thread)
    websocket_thread.start()

    run_ursina_app()