# 메이즈러너 https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description

import sys
input = sys.stdin.readline

def taxi_distance(p1, way_out): #실제 거리와 x, y 거리 간 차이도 반환.
    return abs(p1[0]-way_out[0])+abs(p1[1]-way_out[1]), way_out[0]-p1[0], way_out[1]-p1[1]

def move():
    pop_candidates = []
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
        elif not(graph[runner[0]][runner[1]+y_sign]) and y_sign: 
            runners[r_idx] = [runner[0], runner[1]+y_sign]
        # if runners[r_idx] == way_out:
        #     pop_candidates.append(r_idx)

        #여기 매우 중요. 그냥 빼버리면 돌면서 문제 생길 수 있음
        runners[:] = [runner for runner in runners if runner != way_out]

def rotate():
    rotate_candidate = [N, N, N] # 앞부터 택시거리, x좌표, y좌표
    #회전 기준 러너 찾기
    for runner in runners:
        temp = taxi_distance(runner, way_out)
        if temp[0] < rotate_candidate[0]:
            rotate_candidate = temp
        elif temp[0] == rotate_candidate[0]: #거리 같을 때
            if temp[1] < rotate_candidate[1]: #r좌표 -> x좌표 최우선
                rotate_candidate = temp
            elif temp[1] == rotate_candidate[1]:
                if temp[2] < rotate_candidate[2]:
                    rotate_candidate = temp
    #가장 작은 정사각형 찾기
    if rotate_candidate[1] == rotate_candidate[2]: #최저 r,c에서 최대 r,c로 가는(둘다 증가하는) 사선 점으로 고정해줘야함. 반환.
        square_points = [[min(rotate_candidate[1], way_out[0]), min(rotate_candidate[2], way_out[1])], [max(rotate_candidate[1], way_out[0]), max(rotate_candidate[2], way_out[1])]]
    else:
        #사각형 사이즈부터 견적내자 | 차+1이 사각형 사이즈
        square_size = max(abs(rotate_candidate[2] - way_out[1]), abs(rotate_candidate[1] - way_out[0]))
        max_pos = [max(rotate_candidate[1], way_out[0]), max(rotate_candidate[2], way_out[1])]
        #max pos에서 사각형 사이즈 만큼 뺀게 graph 밖이면 사각형 위치 조정해줘야함. 이거 차만큼 반영하면 무조건 가장 rc를 최소화하면서 다 포함 가능?
        min_pos = [max_pos[0]-square_size, max_pos[1]-square_size] #인덱스가 반드시 둘다 1이상이어야함
        if min_pos[0] <=0 or min_pos[1] <= 0:
            compensate = []
            compensate.append(1-min_pos[0]) if min_pos[0]<=0 else compensate.append(0)
            compensate.append(1-min_pos[1]) if min_pos[1]<=0 else compensate.append(1)
            min_pos = [min_pos[0]+compensate[0], min_pos[1]+compensate[0]]
            max_pos = [max_pos[0]+compensate[0], max_pos[1]+compensate[0]]
            square_points = [min_pos,max_pos]
        else:
            square_points = [min_pos,max_pos]

    #빼내서 회전하면서 내구도 1감소 처리

    
    # return rotated_arr

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

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



#돌릴 때, 범위 설정하고 runners가 그 안에 있으면 임의로 넣어서 같이 돌리고 그 좌표를 재할당
