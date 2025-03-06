from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import asyncio
import numpy as np
import time, os
import threading

small_sphere = np.full((42), None)


def process_data():
    file_name = '인사.txt'
    PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', file_name)

    f = open(PATH, 'r')
    seq_arr = []
    while True:
        line = f.readline().rstrip()
        if not line: break
        seq_arr.append(line.split(','))

            

    rate = -30 # 크기(점 사이 거리) 조절을 위한 값
    while True:
        time.sleep(0.5)
        # print("DEBUG")
        # print(len(seq_arr))
        # print(seq_arr[0][0])
        for frame in seq_arr:
            time.sleep(0.03)
            # print(frame)
            for i in range(21):
                idx = i * 3
                if small_sphere[i] is not None:
                    # small_sphere[i].color = color.yellow
                    small_sphere[i].position = (float(frame[idx])*rate, float(frame[idx+1])*rate, float(frame[idx+2])*rate)
                if small_sphere[i+21] is not None:
                    # small_sphere[i+21].color = color.yellow
                    small_sphere[i+21].position = (float(frame[idx+63])*rate, float(frame[idx+64])*rate, float(frame[idx+65])*rate*2.0)


def run_ursina_app():
    app = Ursina()
    mouse.visible = False
    for i in range(len(small_sphere)):
        small_sphere[i] = Entity(model='sphere', color=color.red, scale=0.5)
    
    main_floor = Entity(model='cube', position=(0,-30,0), scale=(45,1,50), color=color.blue, collider='box')
    player = FirstPersonController()
    player.cursor.visible = False
    player.gravity = 0.5
    player.speed = 15
    # EditorCamera()

    app.run()

async def loop_thread():
    await asyncio.ensure_future(process_data())

if __name__ == "__main__":
    loop_thread_instance = threading.Thread(target=lambda: asyncio.run(loop_thread()))
    loop_thread_instance.start()
    run_ursina_app()
