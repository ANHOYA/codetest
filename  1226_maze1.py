#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV14vXUqAGMCFAYD&categoryId=AV14vXUqAGMCFAYD&categoryType=CODE&problemTitle=1226&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys
from collections import deque
input = sys.stdin.readline

def bfs(maze):
    len_maze = len(maze)
    queue = deque([(1, 1)])
    maze[1][1] = 4
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx>=len_maze or ny<0 or ny>=len_maze:
                continue
            elif maze[nx][ny] == 1 or maze[nx][ny] == 4:
                continue
            elif maze[nx][ny] == 3:
                return 1
            else:
                maze[nx][ny] = 4
                queue.append([nx,ny])
    return 0

#도착가능 1 불가능 0
#상 하 좌 우
dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

for _ in range(10):
    tc = int(input().rstrip())
    maze = [list(map(int, input().rstrip())) for _ in range(16)]
    print(f"#{tc} {bfs(maze)}")
