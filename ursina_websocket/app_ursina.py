from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import asyncio
import websockets
import threading
import numpy as np
import json



small_sphere = np.full((42), None)

async def receive_messages(websocket):
    try:
        hand1 = np.zeros((21,3))
        hand2 = np.zeros((21,3))
        rate = -10 # 크기(점 사이 거리) 조절을 위한 값

        while True:
            message = await websocket.recv()
            data = json.loads(message)  # JSON 형식의 메시지를 딕셔너리로 변환
            # 'hand1'과 'hand2' 키를 가진 딕셔너리에서 값을 추출하여 리스트로 변환하여 hands 변수에 저장
            hand1 = np.array(data['hand1'])
            hand2 = np.array(data['hand2'])
            # print(len(hand1))
            # print("DEBUG")
            # print(hand1)
            # print(hand2)
            # print("DEBUG_END")
            for i in range(len(small_sphere)//2):
                if small_sphere[i] is not None:
                    small_sphere[i].position = (hand1[i][0]*rate, hand1[i][1]*rate, hand1[i][2]*rate)
                if small_sphere[i+21] is not None:
                    small_sphere[i+21].position = (hand2[i][0]*rate, hand2[i][1]*rate, hand2[i][2]*rate)


    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")

async def send_hello(websocket):
    try:
        while True:
            await websocket.send("Hello")
            # print("send")
            await asyncio.sleep(0.06)  # 메시지 주기
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")

async def websocket_thread():
    uri = "ws://localhost:8085/"
    async with websockets.connect(uri) as websocket:
        asyncio.ensure_future(send_hello(websocket))
        await asyncio.ensure_future(receive_messages(websocket))

def run_ursina_app():
    global small_sphere
    app = Ursina()
    mouse.visible = False
    # main_floor = Entity(model='cube', position=(0,0,0), scale=(45,1,50), color=color.gray, collider='box')
    for i in range(len(small_sphere)):
        small_sphere[i] = Entity(model='sphere', color=color.red, scale=0.5)
    # player = FirstPersonController()
    # player.cursor.visible = False
    # player.gravity = 0.5
    # player.speed = 15
    EditorCamera()

    app.run()

if __name__ == "__main__":
    websocket_thread_instance = threading.Thread(target=lambda: asyncio.run(websocket_thread()))
    websocket_thread_instance.start()
    run_ursina_app()
