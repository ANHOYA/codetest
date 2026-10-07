# 메이즈러너 https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description
# 첨삭본: 이동 -> 탈출 처리 -> 정사각형 선택 -> 미로/좌표 회전
# graph에는 숫자(빈칸 0, 벽 내구도)만 저장한다. 참가자와 출구는 별도 좌표로 관리한다.

import sys
input = sys.stdin.readline

def taxi_distance(p1, way_out): # 이동 방향 판단용 맨해튼 거리와 행/열 차이
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
        # 출구에 가까워지는 방향은 각 축마다 하나뿐이다. 상하를 먼저 확인한다.
        if x_sign and not graph[runner[0]+x_sign][runner[1]]:
            runners[r_idx] = [runner[0]+x_sign, runner[1]]
            mileage += 1
        elif y_sign and not graph[runner[0]][runner[1]+y_sign]:
            runners[r_idx] = [runner[0], runner[1]+y_sign]
            mileage += 1
    # 반복 도중 runners를 줄이면 뒤 참가자를 건너뛸 수 있으므로 이동 후 제거한다.
    runners[:] = [runner for runner in runners if runner != way_out]

def find_rotation_base_runner():
    # 후보: (한 변의 좌표 차이, 좌상단 행, 좌상단 열). 실제 칸 수는 첫 값 + 1.
    base_candidate = (N, N, N)
    for runner in runners:
        required_square_size = max(abs(runner[0] - way_out[0]), abs(runner[1] - way_out[1]))
        max_pos = [max(runner[0], way_out[0]), max(runner[1], way_out[1])]
        # 두 점을 포함하면서 좌상단을 가능한 한 위/왼쪽에 둔다.
        min_pos = [max_pos[0] - required_square_size, max_pos[1] - required_square_size]
        if min_pos[0] <= 0 or min_pos[1] <= 0:
            # 1-index 격자 밖으로 나간 축만 안쪽으로 민다.
            compensate = [max(0, 1 - min_pos[0]), max(0, 1 - min_pos[1])]
            min_pos = [min_pos[0] + compensate[0], min_pos[1] + compensate[1]]
        # 튜플은 크기 -> 좌상단 행 -> 좌상단 열 순으로 비교된다.
        base_candidate = min(base_candidate, (required_square_size, min_pos[0], min_pos[1]))
    return base_candidate

def rotate():
    rotate_area = find_rotation_base_runner()
    size, top, left = rotate_area
    # 슬라이스로 기존 숫자들을 먼저 복사해야 graph에 덮어쓰는 중 값이 섞이지 않는다.
    # 끝 인덱스는 포함되지 않으므로 좌표 차이 size에 1을 더한다.
    before_rotate = [row[left:left+size+1] for row in graph[top:top+size+1]]
    # 행 순서를 뒤집고 전치하면 시계 방향 90도 회전이다.
    # 예: [[1,2],[3,4]] -> [[3,1],[4,2]]
    after_rotate = list(map(list, zip(*before_rotate[::-1])))

    # 0은 그대로, 양수인 벽은 1 감소한다.
    for r_idx in range(len(after_rotate)):
        for c_idx in range(len(after_rotate)):
            graph[top+r_idx][left+c_idx] = max(0, after_rotate[r_idx][c_idx]-1)

    # 정사각형 내부의 상대좌표 (r,c)는 시계 방향 회전 후 (c,size-r).
    # 참가자/출구를 graph에 표기하면 원래 칸의 숫자를 잃고, 여러 명이 한 칸에
    # 있을 때 한 명만 남는다. 따라서 좌표를 별도로 바꾼다.
    for runner in runners:
        if top <= runner[0] <= top+size and left <= runner[1] <= left+size:
            r, c = runner[0]-top, runner[1]-left
            runner[:] = [top+c, left+size-r]
    r, c = way_out[0]-top, way_out[1]-left
    # way_out[:]은 기존 리스트를 제자리에서 수정하므로 global 선언이 필요 없다.
    way_out[:] = [top+c, left+size-r]

N, M, K = map(int, input().split())

graph = [[]]
for _ in range(N): #미로 지도
    graph.append([0]+list(map(int, input().split())))
runners = [list(map(int, input().split())) for _ in range(M)] #참가자 좌표
way_out = list(map(int, input().split())) #출구 좌표
mileage = 0

for t in range(1, K+1):
    move()
    # 전원 탈출 시 회전할 정사각형이 없으므로 여기서 종료한다.
    if len(runners) == 0:
        break
    rotate()

#출력 조건은 (모든 참가자들의 이동거리 합 / 출구 좌표)
print(mileage)
print(*way_out)
