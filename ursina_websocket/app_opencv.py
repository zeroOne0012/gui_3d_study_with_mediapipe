
import numpy as np
import cv2
import mediapipe as mp
import time
import threading
import asyncio
import websockets
import json
import time



async def app_opencv(websocket, path):
    try:
        # print("DEBUG??")
        hand1 = np.zeros((21, 3))
        hand2 = np.zeros((21, 3))
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.4,
            min_tracking_confidence=0.4)
        
        cap = cv2.VideoCapture(0)


        while True:
            message = await websocket.recv()
            if not cap.isOpened(): break
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.\n웹캠을 사용중인 프로세스를 중지해주세요.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            result = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 웹캠 화면에 랜드마크 출력
            if result.multi_hand_landmarks:
                for res in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, res, mp_hands.HAND_CONNECTIONS)
            cv2.imshow('img', image)


            data=np.zeros((42,3))
            # 손 좌표 전달
            if result.multi_hand_landmarks:
                h=0
                for res in result.multi_hand_landmarks:
                    h+=1
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]
                    if h==1:
                        hand1 = joint
                    else:
                        hand2 = joint
                if 'hand2' not in locals(): continue
                data = {'hand1': hand1.tolist(), 'hand2': hand2.tolist()}
                result_json = json.dumps(data)
                try:
                    if websocket.open:
                        print("sended!")
                        await websocket.send(result_json)
                except Exception as e:
                    print(f"send error: {str(e)}")

            key = cv2.waitKey(1)
            if key == 27:  # ESC 키를 누르면 루프 종료
                break
    except websockets.exceptions.ConnectionClosedOK:
        pass


start_server = websockets.serve(app_opencv, "localhost", 8085)  


async def main():
    await start_server


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
