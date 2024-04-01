import cv2
import mediapipe as mp
import numpy as np
import time, os

seq_length = 120


secs_for_action = 6 # 초
time_to_start = 1 # 초

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4)

cap = cv2.VideoCapture(0)

created_time = int(time.time())
os.makedirs('dataset', exist_ok=True)

action= None
stop_=False

a=0 # frame debug

print(f'1회 데이터 입력 시간: {secs_for_action}초')
print(f'데이터 입력 시작 시 딜레이: {time_to_start}초')

anounce_for_user = f'''
웹캠 화면에서 메뉴 선택
l 데이터를 쌓을 수어의 한글 단어 입력
. 수어 데이터 입력 시작
t 데이터 입력 시간 변경(default: {secs_for_action}s)
y 데이터 입력 준비 시간 변경(defalut: {time_to_start}s)
ESC 종료
'''
print(anounce_for_user)

while cap.isOpened():
    ###
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.\n웹캠을 사용중인 프로세스를 중지해주세요.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for res in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, res, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('img', image)


    key = cv2.waitKey(1)
    if key == ord('l'):
        # 단어, 라벨 입력
        action = input('단어 입력: ')
        print(f'({action}) 입력 완료')
        # print(anounce_for_user)
    
    if key == ord('t'):
        while True:
            secs_for_action = input(f'{secs_for_action} -> ')
            try:
                secs_for_action = float(secs_for_action)
                break
            except ValueError:
                print("실수 값을 입력해주세요.")            
        print('데이터 입력 시간 변경 완료')

    if key == ord('y'):
        while True:
            time_to_start = input(f'{time_to_start} -> ')
            try:
                time_to_start = float(time_to_start)
                break
            except ValueError:
                print("실수 값을 입력해주세요.")
        print('데이터 입력 준비 시간 변경 완료')
        
    if key == ord('.'):
        if action is None:
            print("l을 눌러 입력할 단어를 설정해주세요.")
            continue
        print(f'({action}): {secs_for_action}초간 데이터 생성을 {time_to_start}초 뒤 시작합니다.')
        print('q: 중단(준비 시간 이후 중단 가능)')
        data = []
        ###
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.putText(img, f'Ready...', org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,0), thickness=2)
        cv2.imshow('img', img)
        cv2.waitKey(int(time_to_start*1000)) 

        start_time = time.time()

        while time.time() - start_time < secs_for_action:
            a+=1
            ret, img = cap.read()

            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if result.multi_hand_landmarks is not None:
                h = 0 # 손 두개 감지 로직을 위한 임시 값
                d1 = np.zeros((21, 3))
                d2 = np.zeros((21, 3))
                if len(result.multi_hand_landmarks) ==1: continue
                for res in result.multi_hand_landmarks:
                    h+=1
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]

                    
                    if h==1:
                        d1 = joint.flatten()
                    else:
                        d2 = joint.flatten()

                    # 파이썬 실행 화면(웹캠)에 랜드마크 그림
                    mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
                d=np.concatenate([d1, d2])
                # print(d[-1], end=' ')
                data.append(d)
                
            cv2.imshow('img', img)
            if cv2.waitKey(1) == ord('q'):
                stop_=True
                break
        if stop_:
            stop_=False
            print("데이터 생성 중단")
            continue
        print("frame: ", a)
        ###
        data = np.array(data)
        print(action, data.shape) #debug
        

        if len(data) - seq_length < 4:
            print("프레임이 너무 적어 데이터 생성에 실패했습니다.")
            continue

        # 시퀀스 데이터 생성
        full_seq_data = []
        
        start_seq = 3

        full_seq_data = data[start_seq:start_seq + seq_length]
        # print(type(full_seq_data)) # np array
        #  # # ###################################################################### 유니티에 e표기 부동소수 적용 가능한지
        

        if len(full_seq_data)==60 and len(full_seq_data[0])==126:
            print('seccess')

        # # list -> numpy
        # full_seq_data = np.array(full_seq_data)
        # print(action, full_seq_data.shape) # debug

        d = full_seq_data.tolist()
        # 저장할 npy 파일 이름
        file_name = str(action) + '.txt'
        print("DEBUG", len(d))
        print(len(d[0]))
        # 저장
        script_directory = os.path.dirname(os.path.abspath(__file__))
        PATH = os.path.join(script_directory, "dataset", file_name)
        ##
        with open(PATH, 'w') as file:
            for line in d:
                file.write(f"{','.join(str(a) for a in line)}\n")
        
        print(f'({action}):', data.shape, full_seq_data.shape, '데이터 생성 완료')

        
        

    if key == 27:  # ESC 키를 누르면 루프 종료
        break
    ###







