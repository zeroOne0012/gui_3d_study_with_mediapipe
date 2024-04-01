from cvzone.ColorModule import ColorFinder
import cvzone
import cv2
import socket

import time

port = 5052

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

success, img = cap.read()
h,w,_ = img.shape # 동적인 코드를 위해 720 직접 사용 x, 반복문 내에서 쓸 고정된 값 미리 구함, 안쓰는 세번째 값은 채널: 컬러 이미지의 경우 3 고정

# ColorFinder: True 일 시 hsv 색상을 찾을 수 있는 gui 창 하나가 추가로 생성됨
myColorFinder = ColorFinder(False) # 색을 찾아야 하면 True, 이미 있다면 False?, Ctrl click으로 hsvVals ex 찾기
hsvVals = {'hmin': 100, 'smin': 13, 'vmin': 137, 'hmax': 128, 'smax': 62, 'vmax': 196}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # family type, type(DGRAM:UDP, STREAM:TCP)
serverAddressPort = ("127.0.0.1", port)

while True:
    time.sleep(0.03)  # 0.03초 동안 딜레이

    success, img = cap.read()

    flipped_image = cv2.flip(img, 1) # 이미지 좌우 대칭

    imgColor, mask = myColorFinder.update(img, hsvVals) # hsvVals 색상만 보이는 화면과 그에 대한 마스크
    imgContour, contours = cvzone.findContours(img, mask, minArea = 1000) # 감지한 물체 윤곽 (contour: 윤곽)

    if contours:
        data = contours[0]['center'][0], \
               h-contours[0]['center'][1], \
               int(contours[0]['area']) # 감지한 물체 중심의 x,y, area?
        print(data)

        data = str.encode(str(data)) # 문자열 -> 바이트 인코딩
        sock.sendto(data, serverAddressPort) # 서버로 전송
        # sock.sendto(str.encode(str(data)), serverAddressPort) # 간단히

    # imgStack = cvzone.stackImages([img, imgColor, mask, imgContour], 2, 0.5) # [원본, hsvVals추출, 추출하는 마스크, 추출한 부위 윤곽]
    # cv2.imshow("Image", imgStack)
    imgContour = cv2.resize(imgContour, (0,0), None, 0.3, 0.3)
    cv2.imshow("ImageContour", imgContour)
    cv2.waitKey(1)


# 통신- TCP, UDP?
# 브로드캐스트에 가까운 UDP는 데이터를 계쏙 전송하게 되며 데이터를 원하는 누구든 볼 수 있음
# TCP는 UDP보다 조금 느리고, UDP는 직접 연결이 필요하지 않으므로 실패 가능성이 적고 충돌 가능성이 적다.
# TCP는 유니티 충돌이 가끔 발생한다고 한다. 어떤 것을 켰을 때 통신이 끊기는 등의 오류가 발생함.
# TCP가 조금 빠르지만 충돌하지 않는 UDP를 사용하기로 한다.
# TCP를 쓰면 디버깅 과정에서 파이썬과 유니티 둘다 껐다가 켜야 하지만, UDP는 파이썬은 켜두고 유니티만 재실행하는 방식으로도 통신을 유지할 수 있다.
    
# 통신 시작하기
# 유니티의 Project에 UDPReceive.cs 생성, Hierarchy에 Create Empty(Manager), Manager의 Inspector 위에 UDPReceive.cs를 올려둔 뒤, 파이썬 유니티 각각 실행 시 좌표가 전송됨을 확인 가능


# Material 적용법
# Hierarchy - 3D Object - Sphere(Ball)
# Assets - Create - Meterial (Green)
# Sphere(Ball) - Inspector - Materials - Green
    
# C# Script(BallMovement) 생성하여 Ball(Inspector)에 드래그로 적용

# Ball에 Component-script(BallMovement.cs) 추가, 코드 작성 후 Ball의 Inspector-BallMovement-Udp Receive에 Manager 끌어다가 올려놓기
    
# 실행하면? 실시간 좌표 반영 성공!
    
# Ctrl \ -> vscode 탭 분할+복사?