# 메이즈러너 https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description

import sys
input = sys.stdin.readline

def taxi_distance(p1, way_out): #실제 거리와 x, y 거리 간 차이도 반환.
    return abs(p1[0]-way_out[0])+abs(p1[1]-way_out[1]), way_out[0]-p1[0], way_out[1]-p1[1]

def move():
    global mileage
    for r_idx, runner in enumerate(runners):
        move_temp = taxi_distance(runner, way_out)
        if move_temp[1] == 0:
            x_sign = 0
        elif move_temp[1] > 0:
            x_sign = 1
        else:
            x_sign = -1
        if move_temp[2] == 0:
            y_sign = 0
        elif move_temp[2] > 0:
            y_sign = 1
        else:
            y_sign = -1
        if x_sign and not graph[runner[0]+x_sign][runner[1]]: # 상하 이동 우선
            runners[r_idx] = [runner[0]+x_sign, runner[1]]
            mileage += 1
        elif y_sign and not graph[runner[0]][runner[1]+y_sign]:
            runners[r_idx] = [runner[0], runner[1]+y_sign]
            mileage += 1

    # 모든 참가자의 이동을 마친 뒤 탈출자를 한꺼번에 제거한다.
    runners[:] = [runner for runner in runners if runner != way_out]

def rotate():
    global way_out
    # 각 참가자와 출구를 포함하는 최소 정사각형의 (크기, 좌상단 행, 열)을 비교한다.
    rotate_candidate = (N + 1, N + 1, N + 1)
    for runner in runners:
        square_size = max(abs(runner[0] - way_out[0]),
                          abs(runner[1] - way_out[1])) + 1
        top = max(1, max(runner[0], way_out[0]) - square_size + 1)
        left = max(1, max(runner[1], way_out[1]) - square_size + 1)
        rotate_candidate = min(rotate_candidate, (square_size, top, left))

    square_size, top, left = rotate_candidate
    square_points = [[top, left], [top + square_size - 1, left + square_size - 1]]

    # 원래 칸을 읽어 시계 방향으로 옮긴 뒤, 회전된 벽의 내구도를 낮춘다.
    rotated_arr = [[0] * square_size for _ in range(square_size)]
    for r in range(square_size):
        for c in range(square_size):
            rotated_arr[c][square_size - 1 - r] = max(0, graph[top + r][left + c] - 1)
    for r in range(square_size):
        for c in range(square_size):
            graph[top + r][left + c] = rotated_arr[r][c]

    for runner in runners:
        if top <= runner[0] <= square_points[1][0] and left <= runner[1] <= square_points[1][1]:
            r, c = runner[0] - top, runner[1] - left
            runner[:] = [top + c, left + square_size - 1 - r]
    r, c = way_out[0] - top, way_out[1] - left
    way_out = [top + c, left + square_size - 1 - r]

N, M, K = map(int, input().split())

graph = [[]]
for _ in range(N): #미로 지도
    graph.append([0]+list(map(int, input().split())))
runners = [list(map(int, input().split())) for _ in range(M)] #참가자 좌표
way_out = list(map(int, input().split())) #출구 좌표
mileage = 0

for t in range(1, K+1):
    move()
    if len(runners) == 0:
        break
    rotate()

print(mileage)
print(*way_out)
