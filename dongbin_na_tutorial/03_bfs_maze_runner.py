import sys
from collections import deque
input = sys.stdin.readline

def bfs(x,y):
    queue = deque()
    queue.append((x,y))
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            #graph 범위 밖 처리
            if nx<0 or nx>=n or ny<0 or ny>=m:
                continue
            #grpah 내 벽에 부딪히면 무시
            elif graph[nx][ny] == 0:
                continue
            #처음 방문하는 경우.
            elif graph[nx][ny] ==1:
                graph[nx][ny] = graph[x][y] + 1
                queue.append((nx,ny))
    return graph[n-1][m-1]
        

n, m = map(int, input().split())
graph = []
for i in range(n):
    graph.append(list(map(int, input().rstrip())))

# 상 하 좌 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

print(bfs(0,0))