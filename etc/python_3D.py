# https://www.youtube.com/watch?v=73Xevu1DVyg 11분 즘 텔레포트 전까지의 내용. ursina 기본 사용법

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController # 1인칭 컨트롤러
# EditorCamera()나 FirstPersonController()로 화면 이동 방법 결정

app = Ursina()
mouse.visible = False # 컴퓨터 마우스 없애기

main_floor = Entity(model = 'cube', position=(0,0,0), scale=(45,1,50), color = color.gray, collider = 'box')
# Entity 무늬/그림 넣기: texture = 'assets/wall.jpg'
# 텍스처 늘어나지 않게: texture_scale=(원본가로,원본세로)

# EditorCamera()
player = FirstPersonController() # 조작: WASD, Space, mouse
player.cursor.visible = False # 커서 없애기
player.gravity = 0.5 # 중력
player.speed = 15 # 속도 변경 (기본값 10?)

app.run()
