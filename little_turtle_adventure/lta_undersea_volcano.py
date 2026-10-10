#https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/a-little-sea-turtles-big-adventure/description

import sys, math
from collections import deque
input = sys.stdin.readline

# NxN격자 / 안석차는 N-1, N-1에 위치 / 최대 100턴
# 각 턴은 4단계 구성
# 0. find path
# 1. Move
# 2. 화산 마그마 압력 10씩 증가
# 3. 화산 분출 및 연쇄 반응
# 4. 환경 초기화 ( 열기 정보 제거, 압력 0으로 초기화 ) 

#이동은 최단 경로로 움직인다. 
# 이때, 경로가 여러개라면 첫 이동방향이 우 하 좌, 상 순서로 우선순위
# 최단 경로가 존재하지 않으면 정지
# 경로 탐색은 매거북이마다 움직이고 update해야함

#움직일때, 화석과 산호초는 통과 불가
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]
# 시작을 종점부터해서 

def find_path(t_idx): #bfs 식으로 구성해야할듯
    global turtles, isturtlealive, graph, N
    local_graph = [row[:] for row in graph]
    if isturtlealive[t_idx] == False:
        return None
    isvisited = [[False]*N for _ in range(N)]
    pos_turtle = turtles[t_idx]
    queue = deque()
    # pos_start = turtles[t_idx]
    pos_start = [N-1,N-1]
    queue.append(pos_start)
    isvisited[pos_start[0]][pos_start[1]] = True
    local_graph[pos_start[0]][pos_start[1]] = -1
    while queue:
        ego = queue.popleft()
        for i in range(4):
            nr, nc = ego[0] + dr[i], ego[1] + dc[i]
            #graph 범위 탐색
            if nr < 0 or nr >= N or nc <0 or nc >= N:
                continue
            #산호초가 있는지 check
            elif graph[nr][nc] == 1:
                continue
            #마지막이어도 스킵해도 되지 않나?
            if nr == pos_turtle[0] and nc == pos_turtle[1]:
                isvisited[nr][nc] = True
                continue
            # 다른 turtle이 있는지, 방문했었는지 check
            isthereturtle = False
            for t_loc_idx, j_turtle in enumerate(turtles):
                if t_idx == t_loc_idx:
                    continue
                if j_turtle[0] == nr and j_turtle[1] == nc:
                    isthereturtle = True
            if isthereturtle or isvisited[nr][nc]:
                continue
            #방문처리 해주고. -1
            
                
            isvisited[nr][nc] = True
            local_graph[nr][nc] = local_graph[ego[0]][ego[1]] -1
            queue.append([nr,nc])

    
    result = None
    temp = N**2
    for j in range(4):
        nr, nc = pos_turtle[0] + dr[j], pos_turtle[1] + dc[j]
        if nr < 0 or nr >= N or nc <0 or nc >= N:
            continue
        if (((-1)*local_graph[nr][nc]) > 0) and (((-1)*local_graph[nr][nc])<temp):
            result = j
            temp = (-1)*local_graph[nr][nc]
    return result # 방향 dr, dc의 인덱스 순으로 제공
    # 이동 없다면 None, 이동 있다면 j 방향 인덱스로 제공


def move(t_idx):
    dir = find_path(t_idx)
    if dir != None:
        turtles[t_idx] = [ turtles[t_idx][0] + dr[dir], turtles[t_idx][1] + dc[dir], turtles[t_idx][2]+1 ]

def increase_pressure():
    global volcano_status, volcanos
    judge = deque()
    for v_idx in range(len(volcano_status)):
        volcano_status[v_idx] += 10
        if volcanos[v_idx][2] <= volcano_status[v_idx]:
            judge.append(v_idx)
    return judge

def erupt(erupting_volcanos): #인덱스로 터질 화산 들어오는 거임
    global eruptionmap, volcanos, graph
    #초기화 과정 이후에는 다시 계산 안 하고 그냥 불러오면 되니까
    local_eruption_graph = [[0]*N for _ in range(N)]
    while erupting_volcanos:
        ego_idx = erupting_volcanos.popleft()
        ego = volcanos[ego_idx]
        local_eruption_graph[ego[0]][ego[1]] = ego_pressure
        for i in range(4):
            ego_pressure = volcano_status[ego_idx]
            nr, nc = ego[0] + dr[i], ego[1] + dc[i]
            for _ in range(N):
                #graph 범위 탐색
                if nr < 0 or nr >= N or nc <0 or nc >= N or graph[nr][nc] == 1:
                    break
                local_eruption_graph[nr][nc] += math(ego_pressure/2).floor()
                for p_idx, vol in enumerate(pos_volcanos):
                    temp = volcano_status[p_idx]+local_eruption_graph[nr][nc]
                    #nr, nc가 화산이면서 임계치를 넘는 값을 가지게 되면..
                    if [nr, nc] == vol and temp >= volcano_status[p_idx][2]:
                        erupting_volcanos.append(p_idx)
                nr, nc = nr + dr[i], nc + dc[i]
    return local_eruption_graph
                
                
    

def fossil():
    pass

def initialize():
    pass

#입력 N / 거북수 M / 화산 수 K
# N개의 줄에 바다 공간 정보 0 빈공간 1산호초
# M개 줄에 초기 위치 r,c가 

N, M, K = map(int, input().split())
graph = [] #좌상단 0,0 우하단 안식처 N-1, N-1
for _ in range(N):
    graph.append(list(map(int, input().split())))
turtles=[] #r,c
isturtlealive=[True]*M
for _ in range(M):
    turtles.append(list(map(int, input().split()))+[0])

volcanos = []
volcano_status = [0] * K
for _ in range(K):
    volcanos.append(list(map(int, input().split())))
pos_volcanos = []
for vol in volcanos:
    pos_volcanos.append([vol[0], vol[1]])

for step in range(100):
    for t_idx, aturtle in enumerate(turtles):
        move(t_idx)
    temp_eruption = increase_pressure() #v_idx 로 터지는 화산 제공
    if temp_eruption != []:
        print(erupt(temp_eruption))
    
    #turtle 도착 여부 check 다 도착했으면 즉시 종료
    # 다 죽었어도 즉시 종료
    # 살아있는 turtle만 move 움직여주기
    #
    pass
#출력조건은 매 거북이마다 100턴 내 바다거북이 도착 못하거나 도중 화석 -1
#도착했으면 도착한 턴 번호 출력