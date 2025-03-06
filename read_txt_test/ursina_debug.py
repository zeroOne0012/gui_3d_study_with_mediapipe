from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import asyncio
import numpy as np
import time, os
import threading

small_sphere = np.full((19), None)


std_example = [
        [355, 184],
        [364, 174],
        [347, 175],
        [394, 250],
        [326, 247],
        [399, 331],
        [319, 325],
        [399, 399],
        [314, 392],
        [379, 405],
        [338, 403],
        [372, 502],
        [338, 505],
        [371, 591],
        [338, 589],
        [367, 601],
        [344, 599],
        [376, 634],
        [328, 633],
    ]
rate = -1/60.0 # 크기(점 사이 거리) 조절을 위한 값

# def process_data():


            

#     while True:
#         time.sleep(10)
#         # print("DEBUG")
#         # print(len(seq_arr))
#         # print(seq_arr[0][0])
#         for i in range(len(std_example)):
#             # time.sleep(0.03)
#             # print(frame)
#             if small_sphere[i] is not None:
#                 # small_sphere[i].color = color.yellow
#                 small_sphere[i].position = (std_example[i][0]*rate, std_example[i][1]*rate, 0)


def run_ursina_app():
    app = Ursina()
    mouse.visible = False
    for i in range(len(std_example)):
        std_example[i] = Entity(model='sphere', color=color.red, scale=0.5, position = (std_example[i][0]*rate, std_example[i][1]*rate, 0))
    # for i in range(len(std_example)):
    #     # time.sleep(0.03)
    #     # print(frame)
    #     print(small_sphere[i] is not None)
    #     if small_sphere[i] is not None:
    #         # small_sphere[i].color = color.yellow
    #         small_sphere[i].position = (std_example[i][0]*rate, 10, 0)
    # main_floor = Entity(model='cube', position=(0,-30,0), scale=(45,1,50), color=color.blue, collider='box')
    # player = FirstPersonController()
    # player.cursor.visible = False
    # player.gravity = 0.5
    # player.speed = 15
    EditorCamera()

    app.run()

# async def loop_thread():
#     await asyncio.ensure_future(process_data())

if __name__ == "__main__":
    # loop_thread_instance = threading.Thread(target=lambda: asyncio.run(loop_thread()))
    # loop_thread_instance.start()
    run_ursina_app()
