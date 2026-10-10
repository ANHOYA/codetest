#https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/a-little-sea-turtles-big-adventure/description
# lta_undersea_volcano.py 첨삭본 (원본 구조 유지: find_path / move / increase_pressure / erupt / fossil / initialize / 메인 루프)

# =====================================================================
# [첨삭 요약] 원본에서 고친 것
#  1. erupt: ego_pressure 를 정의 전에 사용 -> UnboundLocalError
#  2. erupt: math(x).floor() 는 문법 오류 -> 정수 나눗셈 // 사용 (⌊x/2⌋ = x // 2, 양수일 때)
#  3. erupt: 화산 칸 열기는 "압력"이 아니라 "임계치 P" 만큼, 전파는 "이전 칸 열기의 절반"씩 줄어듦
#           (원본은 모든 칸에 같은 값 floor(압력/2)를 더함) + 열기가 0이 되면 전파 중단 조건 누락
#  4. erupt: volcano_status[p_idx][2] -> int 에 인덱싱 (TypeError). 임계치는 volcanos[p_idx][2]
#  5. erupt: 이미 분출한 화산이 다시 큐에 들어갈 수 있음 -> erupted 배열로 중복 방지
#  6. find_path: 도착/화석 거북이 구분이 없음. 장애물 = "살아있는 다른 거북" + "화석"
#               (도착한 거북은 지도에서 제외 -> 장애물 아님)
#  7. move: 안식처 도착 처리(도착 턴 기록, 지도에서 제외)가 없었음
#  8. fossil / initialize 미구현, 출력 없음, 메인 루프에서 죽은/도착한 거북도 move 호출
#  9. step 은 0부터 돌지만 출력 턴 번호는 1부터 -> turn = step + 1
# 
# 
# [시험장 체크리스트]
#  - range(100) 의 step 은 0-based. 출력할 턴 번호가 1부터인지 반드시 확인 (off-by-one 단골)
#  - deque 를 [] 와 == 로 비교하면 비어 있어도 항상 False. 비었는지는 if q: / if not q: 로 검사
#  - 상태가 여러 개인 객체(거북: 이동중/도착/화석)는 bool 하나로 뭉개지 말고 상태를 분리할 것
#    "장애물인가?" 와 "아직 움직이는가?" 는 다른 질문이다
#  - 연쇄 반응은 큐 + visited(erupted) 패턴. 큐에 넣는 순간 True 로 마킹해야 중복 삽입이 안 된다
#  - 리스트 비교 [nr, nc] == vol 같은 건 실수 나기 쉬움. 좌표는 튜플/개별 변수로 비교
#  - 최단경로 + 첫 방향 우선순위 문제는 "목적지에서 BFS -> 거북 주변 4칸 중 dist 최소 & 우선순위 순" 이 정석
#    (거북에서 BFS 하면 첫 방향 추적이 번거로움). 동률일 때 '<' 로 비교해야 먼저 본 방향(우하좌상)이 유지됨
#  - 매 턴 상태 초기화(열기 지도, 분출 화산 압력 0) 빼먹지 말 것
#  - 함수 안에서 전역 리스트 "원소 수정"은 global 필요 없음. 전역 변수 "재할당"할 때만 global 필요
# =====================================================================

import sys
from collections import deque
input = sys.stdin.readline

# NxN격자 / 안식처는 N-1, N-1에 위치 / 최대 100턴
# 각 턴은 4단계 구성
# 1. Move (ID 순서대로, 매 거북이마다 경로 새로 탐색 -> 앞 거북 이동이 즉시 반영)
# 2. 화산 마그마 압력 10씩 증가
# 3. 화산 분출 및 연쇄 반응 + 화석화
# 4. 환경 초기화 ( 열기 정보 제거, 분출한 화산 압력 0으로 초기화 )

#이동은 최단 경로로 움직인다.
# 이때, 경로가 여러개라면 첫 이동방향이 우 하 좌, 상 순서로 우선순위
# 최단 경로가 존재하지 않으면 정지

#움직일때, 산호초 / 다른 살아있는 거북 / 화석은 통과 불가. 화산 칸은 통과 가능
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]
# 시작을 종점부터해서 BFS -> 각 칸에 "안식처까지 거리"를 음수로 기록

def is_blocked(r, c, t_idx):
    # [첨삭] 장애물 판정을 함수로 분리. 원본은 BFS 안에서 모든 거북을 장애물로 봤음
    for o_idx in range(M):
        if o_idx == t_idx:
            continue
        # 이동 중인 다른 거북 or 화석 -> 장애물 / 도착한 거북 -> 지도에서 제외됐으므로 통과
        if (isturtlealive[o_idx] or isfossil[o_idx]) and turtles[o_idx][0] == r and turtles[o_idx][1] == c:
            return True
    return False

def find_path(t_idx): #bfs 식으로 구성
    local_graph = [row[:] for row in graph]
    if isturtlealive[t_idx] == False:
        return None
    isvisited = [[False]*N for _ in range(N)]
    pos_turtle = turtles[t_idx]
    queue = deque()
    pos_start = [N-1, N-1]
    queue.append(pos_start)
    isvisited[pos_start[0]][pos_start[1]] = True
    local_graph[pos_start[0]][pos_start[1]] = -1  # 안식처 = -1, 한 칸 멀어질수록 -1씩 (거리 = -값)
    # [시험장] 이렇게 graph 값과 거리를 한 배열에 섞어 쓰면 0(빈칸)/1(산호초)와 헷갈리기 쉽다.
    #          dist = [[-1]*N for _ in range(N)] 처럼 거리 전용 배열을 따로 두는 게 안전함
    while queue:
        ego = queue.popleft()
        for i in range(4):
            nr, nc = ego[0] + dr[i], ego[1] + dc[i]
            #graph 범위 탐색
            if nr < 0 or nr >= N or nc < 0 or nc >= N:
                continue
            #산호초가 있는지 check
            elif graph[nr][nc] == 1:
                continue
            # 거북 자신의 칸은 더 확장할 필요 없음 (주변 4칸 거리만 알면 됨)
            if nr == pos_turtle[0] and nc == pos_turtle[1]:
                isvisited[nr][nc] = True
                continue
            # 다른 살아있는 거북 / 화석 있는지, 방문했었는지 check
            if isvisited[nr][nc] or is_blocked(nr, nc, t_idx):
                continue
            #방문처리 해주고. -1
            isvisited[nr][nc] = True
            local_graph[nr][nc] = local_graph[ego[0]][ego[1]] - 1
            queue.append([nr, nc])

    result = None
    temp = N**2 + 1
    for j in range(4):  # 우 하 좌 상 순서로 보고, '<' 비교라 동률이면 먼저 본 방향 유지
        nr, nc = pos_turtle[0] + dr[j], pos_turtle[1] + dc[j]
        if nr < 0 or nr >= N or nc < 0 or nc >= N:
            continue
        if (((-1)*local_graph[nr][nc]) > 0) and (((-1)*local_graph[nr][nc]) < temp):
            result = j
            temp = (-1)*local_graph[nr][nc]
    return result # 방향 dr, dc의 인덱스 순으로 제공
    # 이동 없다면 None, 이동 있다면 j 방향 인덱스로 제공


def move(t_idx, turn):
    dir = find_path(t_idx)
    if dir != None:
        turtles[t_idx] = [turtles[t_idx][0] + dr[dir], turtles[t_idx][1] + dc[dir]]
        # [첨삭] 안식처 도착 -> 즉시 지도에서 제외 + 도착 턴 기록
        if turtles[t_idx][0] == N-1 and turtles[t_idx][1] == N-1:
            isturtlealive[t_idx] = False
            arrive_turn[t_idx] = turn

def increase_pressure():
    judge = deque()
    for v_idx in range(K):
        volcano_status[v_idx] += 10
        if volcanos[v_idx][2] <= volcano_status[v_idx]:
            judge.append(v_idx)
    return judge

def erupt(erupting_volcanos): #인덱스로 터질 화산 들어오는 거임
    local_eruption_graph = [[0]*N for _ in range(N)]
    # [첨삭] 큐에 넣는 순간 True -> 같은 화산이 두 번 분출하지 않음
    erupted = [False]*K
    for v_idx in erupting_volcanos:
        erupted[v_idx] = True
    while erupting_volcanos:
        ego_idx = erupting_volcanos.popleft()
        ego = volcanos[ego_idx]
        ego_pressure = ego[2]  # [첨삭] 화산 칸 열기 = 임계치 P (현재 압력 아님), 사용 전에 정의
        local_eruption_graph[ego[0]][ego[1]] += ego_pressure
        for i in range(4):
            heat = ego_pressure // 2  # [첨삭] 방향마다 P 에서 다시 시작
            nr, nc = ego[0] + dr[i], ego[1] + dc[i]
            while True:
                #graph 범위 / 산호초 / 열기 0 이면 해당 방향 전파 중단
                if nr < 0 or nr >= N or nc < 0 or nc >= N or graph[nr][nc] == 1 or heat == 0:
                    break
                local_eruption_graph[nr][nc] += heat
                heat //= 2  # 한 칸마다 이전 칸 열기의 절반
                nr, nc = nr + dr[i], nc + dc[i]
        # 연쇄 반응: 아직 안 터진 화산 중 (압력 + 누적 열기) >= P 이면 분출
        # (열기는 누적만 되므로 확인 순서와 상관없이 최종적으로 터지는 화산 집합은 같다)
        for p_idx, vol in enumerate(volcanos):
            if erupted[p_idx]:
                continue
            if volcano_status[p_idx] + local_eruption_graph[vol[0]][vol[1]] >= vol[2]:
                erupted[p_idx] = True
                erupting_volcanos.append(p_idx)
    return local_eruption_graph, erupted


def fossil(eruption_graph):
    # 모든 분출 끝난 뒤, 살아있는(이동 중인) 거북 칸 열기 >= 20 이면 화석
    for t_idx in range(M):
        if isturtlealive[t_idx] and eruption_graph[turtles[t_idx][0]][turtles[t_idx][1]] >= 20:
            isturtlealive[t_idx] = False
            isfossil[t_idx] = True  # 자리에 고정, 이후 장애물

def initialize(erupted):
    # 열기 지도는 erupt 에서 매 턴 새로 만드므로 따로 지울 필요 없음
    # 분출한 화산만 압력 0, 나머지는 유지
    for v_idx in range(K):
        if erupted[v_idx]:
            volcano_status[v_idx] = 0

#입력 N / 거북수 M / 화산 수 K
# N개의 줄에 바다 공간 정보 0 빈공간 1산호초
# M개 줄에 초기 위치 r,c
# K개 줄에 화산 r, c, P

N, M, K = map(int, input().split())
graph = [] #좌상단 0,0 우하단 안식처 N-1, N-1
for _ in range(N):
    graph.append(list(map(int, input().split())))
turtles = [] #r,c
isturtlealive = [True]*M   # 아직 이동 중 (도착 X, 화석 X)
isfossil = [False]*M       # [첨삭] 화석 여부 따로 관리 (장애물 판정에 필요)
arrive_turn = [-1]*M       # [첨삭] 출력값. 기본 -1 로 두면 미도착/화석 처리가 자동
for _ in range(M):
    turtles.append(list(map(int, input().split())))

volcanos = []  # r, c, P
volcano_status = [0] * K  # 현재 마그마 압력
for _ in range(K):
    volcanos.append(list(map(int, input().split())))

for step in range(100):
    turn = step + 1  # [첨삭] 출력 턴 번호는 1부터
    # 살아있는 turtle만 move 움직여주기 (find_path 안에서도 걸러짐)
    for t_idx in range(M):
        if isturtlealive[t_idx]:
            move(t_idx, turn)
    temp_eruption = increase_pressure() #v_idx 로 터지는 화산 제공
    if temp_eruption:  # [첨삭] deque 는 [] 와 == 비교하면 항상 False -> truthiness 로 검사
        eruption_graph, erupted = erupt(temp_eruption)
        fossil(eruption_graph)
        initialize(erupted)

    # 다 도착했거나 화석이 됐으면 즉시 종료
    if not any(isturtlealive):
        break

#출력조건은 매 거북이마다 100턴 내 바다거북이 도착 못하거나 도중 화석 -1
#도착했으면 도착한 턴 번호 출력
for t_idx in range(M):
    print(arrive_turn[t_idx])
