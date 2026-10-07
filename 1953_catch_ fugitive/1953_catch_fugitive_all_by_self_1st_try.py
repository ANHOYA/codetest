#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5PpLlKAQ4DFAUq&categoryId=AV5PpLlKAQ4DFAUq&categoryType=CODE&problemTitle=1953&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1
# 해당 코드로는 D -> A
#                |
#            C - B   D,C도 연결되어있다고 판단할 수 있음.

import sys
input = sys.stdin.readline
from collections import deque

#상하좌우 연결상태
structure = ([], [1,1,1,1],[1,1,0,0],[0,0,1,1],[1,0,0,1],[0,1,0,1],[0,1,1,0],[1,0,1,0])
structure_connection = ([1,0],[0,1],[2,3],[3,2]) #[structure에서 검사해야할 index 순서로 설계]상으로 갔을 땐 하 / 하로 갔을 땐 상 / 좌로 갔을 땐 우 / 우로갔을 땐 좌

#상하좌우
dr = [1, -1, 0, 0]
dc = [0, 0, -1, 1]

def isstructureconnected(start,end,dir): #출발, 끝, 방향(1,2,3,4) : 상하좌우
    global structure
    j1, j2 = structure_connection[dir]
    if structure[start][j1] == 1 and structure[end][j2] == 1:
        return True
    else:
        return False
    
def make_dfs_graph():
    global info_map, R, C, N, M
    graph = [[False]*M for _ in range(N)]
    queue = deque()
    graph[R][C] = True
    queue.append([R,C])
    while queue:
        r, c = queue.popleft()
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if nr<0 or nc<0 or nr >= N or nc >= M:
                continue
            if graph[nr][nc] == True or info_map[nr][nc]==0:
                continue
            if graph[nr][nc] == False and isstructureconnected(info_map[r][c],info_map[nr][nc],i):
                graph[nr][nc] = True
                queue.append([nr,nc])
    return graph

def how_far_from_hole(hole_r,hole_c):
    global graph, L
    queue = deque()
    queue.append([hole_r,hole_c])
    graph[hole_r][hole_c] = 1
    movable_cnt = 0
    while queue:
        r,c = queue.popleft()
        if graph[r][c] <= L:
            movable_cnt += 1
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if nr<0 or nc<0 or nr >= N or nc >= M:
                continue
            temp = graph[nr][nc]
            if type(temp) == int:
                continue
            if temp == True:
                graph[nr][nc] = graph[r][c] + 1
                queue.append([nr,nc])
    return movable_cnt
#테스트 케이스 개수
tc = int(input().rstrip())

for case in range(tc):
    #N,M<R,C,L( 탈출 후 소요된 시간 L)
    N,M,R,C,L = map(int, input().split())
    info_map = [list(map(int, input().split())) for _ in range(N)]
    graph = make_dfs_graph()
    print(f"#{case+1} {how_far_from_hole(R,C)}")