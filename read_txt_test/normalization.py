import math
from datetime import datetime
import os
import ast

index = {
    0: 0,
    1: 1,
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10:10,
    11:11,
    12:12,
    13:13,
    14:14,
    15:15,
    16:16,
    17:17,
    18:18,
    19:19,
    20:20
}  # 관절번호 인덱스 치환

order = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),
]  # 관절 접근 순서(트리구조)

BODY_PARTS = {
    "NOSE": 0,
    "LEFT_EYE": 2,
    "RIGHT_EYE": 5,
    "LEFT_SHOULDER": 11,
    "RIGHT_SHOULDER": 12,
    "LEFT_ELBOW": 13,
    "RIGHT_ELBOW": 14,
    "LEFT_WRIST": 15,
    "RIGHT_WRIST": 16,
    "LEFT_HIP": 23,
    "RIGHT_HIP": 24,
    "LEFT_KNEE": 25,
    "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27,
    "RIGHT_ANKLE": 28,
    "LEFT_HEEL": 29,
    "RIGHT_HEEL": 30,
    "LEFT_FOOT_INDEX": 31,
    "RIGHT_FOOT_INDEX": 32,
}

def normalization_setting(first_landmarks):
    # 정규화 하기 전에 실행 -> 각 관절별로 비율을 저장
    global ratios, root, tree, different
    ratios = []

    user_example = first_landmarks
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

    different = (
        user_example[0][0] - std_example[0][0],
        user_example[0][1] - std_example[0][1],
    )

    user_landmark = []
    std_landmark = []

    # 튜플로 제공된 데이터 리스트로 가공
    for i in range(19):
        user_landmark.append([user_example[i][0], user_example[i][1]])
        std_landmark.append(
            [std_example[i][0] + different[0], std_example[i][1] + different[1]]
        )

    # 탐색 순서 트리 구조
    def build_tree(order):
        tree = {}
        # 부모-자식 관계를 딕셔너리에 저장
        for parent, child in order:
            if parent not in tree:
                tree[parent] = []
            tree[parent].append(child)

        return tree

    def calculate_distance(point1, point2):
        """두 점 사이의 거리를 계산합니다."""
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_ratio(root, tree, user_landmark, std_landmark):
        calculate_result = []

        # 재귀적으로 전위탐색 수행
        def traverse(node):
            nonlocal calculate_result
            if node in tree:
                for child in tree[node]:
                    user_kp1 = user_landmark[index[node]]
                    user_kp2 = user_landmark[index[child]]
                    std_kp1 = std_landmark[index[node]]
                    std_kp2 = std_landmark[index[child]]
                    result = calculate_distance(std_kp1, std_kp2) / calculate_distance(
                        user_kp1, user_kp2
                    )
                    calculate_result.append(result)
                    traverse(child)

        traverse(root)
        return calculate_result

    root = 0
    tree = build_tree(order)
    ratios = calculate_ratio(root, tree, user_landmark, std_landmark)


def normalizaition(normalize_data):
    # 정규화: 선수 골격을 사용자에 맞춤
    std_landmarks = []  # 전체 사이클
    for landmarks in normalize_data:
        std_landmark = []  # 한 사이클

        # 튜플로 제공된 데이터 리스트로 가공
        for i in range(19):
            std_landmark.append(
                [landmarks[i][0] + different[0], landmarks[i][1] + different[1]]
            )

        def normalize_keypoints(std_kp1, std_kp2, ratio):
            if ratio > 1:
                Px = (std_kp2[0] + ratio * std_kp1[0]) / (1 + ratio)
                Py = (std_kp2[1] + ratio * std_kp1[1]) / (1 + ratio)
            elif ratio < 1:
                Px = (std_kp2[0] - (1 - ratio) * std_kp1[0]) / (1 - (1 - ratio))
                Py = (std_kp2[1] - (1 - ratio) * std_kp1[1]) / (1 - (1 - ratio))
            else:
                Px, Py = std_kp2
            return [Px, Py]

        # 정규화
        def normalize(root, tree, std_landmark):
            # 재귀적으로 전위탐색 수행
            def traverse(node):
                if node in tree:
                    for child in tree[node]:
                        std_kp1 = std_landmark[index[node]]
                        std_kp2 = std_landmark[index[child]]
                        ratio = ratios[index[node]]
                        result = normalize_keypoints(std_kp1, std_kp2, ratio)
                        std_landmark[index[child]] = result
                        parallel_move(child, tree, std_landmark, std_kp2, result)
                        traverse(child)

            traverse(root)

        def parallel_move(root, tree, std_landmark, std_kp2, result):
            diff = (result[0] - std_kp2[0], result[1] - std_kp2[1])

            # 재귀적으로 전위탐색 수행
            def traverse(node):
                if node in tree:
                    for child in tree[node]:
                        Px, Py = std_landmark[index[child]]
                        temp_x = Px + diff[0]
                        temp_y = Py + diff[1]
                        std_landmark[index[child]] = [temp_x, temp_y]
                        traverse(child)

            traverse(root)

        normalize(root, tree, std_landmark)

        std_dict = {}

        for i, line in enumerate(std_landmark):
            body_part = list(BODY_PARTS.keys())[i]

            std_key = body_part
            std_value = line
            std_dict[std_key] = std_value

        std_landmarks.append(std_dict)

    # print(std_landmarks)

    save_txt("normalize_result", std_landmarks)