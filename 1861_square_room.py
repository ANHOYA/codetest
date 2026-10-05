#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5LtJYKDzsDFAXc&categoryId=AV5LtJYKDzsDFAXc&categoryType=CODE&problemTitle=1861&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys

input = sys.stdin.readline

def dfs(x,y):
    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if nx <0 or ny<0 or nx>=N or ny>=N:
            continue
        if graph_visited[nx][ny] or graph[nx][ny]<graph[x][y]:
            continue


#주변을 모두 방문했으면 종료



#상 하 좌 우
dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

tc = int(input().rstrip())
for case in range(tc):
    N = int(input().rstrip())
    final_result = [0, 0]  # start point, movable_stages
    graph = [list(map(int, input().split())) for _ in range(N)]
    graph_visited = [[False]*N for _ in range(N)]
    queue = []
    for r_idx, row in enumerate(graph):
        for c_idx, k in enumerate(row):
            result = 0
            if k > N:
                continue
            else:
                queue.append([r_idx, c_idx])
    for x,y in queue:
        result = 0
        temp = dfs(x,y)
        if temp >= final_result[1]:
            final_result = [[x,y], temp]

    print(graph, graph_visited)
    print(f"#{case+1} {final_result[0]} {final_result[1]}")