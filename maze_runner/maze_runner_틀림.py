# 메이즈러너 https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description

import sys
input = sys.stdin.readline

def taxi_distance(p1, way_out): #실제 거리와 x, y 거리 간 차이도 반환.
    return abs(p1[0]-way_out[0])+abs(p1[1]-way_out[1]), way_out[0]-p1[0], way_out[1]-p1[1]

def move():
    # pop_candidates = []
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
        if not(graph[runner[0]+x_sign][runner[1]]) and x_sign: #상화좌우 모두 다 움직일 수 있으면 이게 우선이지/ x가 상하임
            runners[r_idx] = [runner[0]+x_sign, runner[1]]
            mileage += 1
        elif not(graph[runner[0]][runner[1]+y_sign]) and y_sign: 
            runners[r_idx] = [runner[0], runner[1]+y_sign]
            mileage += 1
        # if runners[r_idx] == way_out:
        #     pop_candidates.append(r_idx)

        #여기 매우 중요. 그냥 빼버리면 돌면서 문제 생길 수 있음
    runners[:] = [runner for runner in runners if runner != way_out]

def find_rotation_base_runner():
    base_candidate = (N, N, N) # 정사각형의 (한 변의 좌표 차이, 좌상단 r, 좌상단 c)
    for runner in runners:
        required_square_size = max(abs(runner[0] - way_out[0]), abs(runner[1] - way_out[1]))
        max_pos = [max(runner[0], way_out[0]), max(runner[1], way_out[1])]
        min_pos = [max_pos[0] - required_square_size, max_pos[1] - required_square_size]
        if min_pos[0] <= 0 or min_pos[1] <= 0:
            compensate = [max(0, 1 - min_pos[0]), max(0, 1 - min_pos[1])]
            min_pos = [min_pos[0] + compensate[0], min_pos[1] + compensate[1]]
        base_candidate = min(base_candidate, (required_square_size, min_pos[0], min_pos[1]))
    return base_candidate

def rotate():
    rotate_area = find_rotation_base_runner() # 정사각형의 (한 변의 좌표 차이, 좌상단 r, 좌상단 c)
    local_graph = graph
    for runner in runners:
        local_graph[runner[0]][runner[1]] = runner
    local_graph[way_out[0]][way_out[1]] = "exit"
    before_rotate = [row[rotate_area[2]:rotate_area[2]+rotate_area[0]+1] for row in local_graph[rotate_area[1]:rotate_area[1]+rotate_area[0]+1]]
    after_rotate = list(map(list, zip(*before_rotate[::-1])))
    #돌리고 나서 숫자 1씩 깍기
    for r_idx , row in enumerate(after_rotate):
        for c_idx, c in enumerate(row):
            if type(c) == int and c>0:
                after_rotate[r_idx][c_idx] -=1
            elif type(c) == list:
                for run_idx, runner in enumerate(runners):
                    if runner == c:
                        runners[run_idx] = [r_idx+rotate_area[1], c_idx+rotate_area[2]]
                after_rotate[r_idx][c_idx] = 0
            elif c == "exit":
                way_out[:] = [r_idx+rotate_area[1], c_idx+rotate_area[2]]
                after_rotate[r_idx][c_idx] = 0

    #원 그래프에 반환
    for r_idx in range(len(after_rotate)):
        for c_idx in range(len(after_rotate)):
            graph[r_idx+rotate_area[1]][c_idx+rotate_area[2]] = after_rotate[r_idx][c_idx]
        
    

    # return rotated_arr

N, M, K = map(int, input().split())

graph = [[]]
for _ in range(N): #미로 지도
    graph.append([0]+list(map(int, input().split())))
runners = [list(map(int, input().split())) for _ in range(M)] #참가자 좌표
way_out = list(map(int, input().split())) #출구 좌표
time = mileage = 0

for t in range(1, K+1):
    move()
    rotate()
    if len(runners) == 0:
        break

#출력 조건은 (모든 참가자들의 이동거리 합 / 출구 좌표)
print(mileage)
print(*way_out)
