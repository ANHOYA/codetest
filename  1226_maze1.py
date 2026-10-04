#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV14vXUqAGMCFAYD&categoryId=AV14vXUqAGMCFAYD&categoryType=CODE&problemTitle=1226&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys
from collections import deque
input = sys.stdin.readline

def bfs(maze):
    len_maze = len(maze)
    ego = [1,1]
    maze[1][1] = 4
    queue.append(ego)
    while queue:
        queue.popleft()
        for i in range(4):
            nx = ego[0]+dx[i]
            ny = ego[1]+dy[i]
            if maze[nx][ny] == 3:
                return 1
            elif maze[nx][ny]==1 or nx < 0 or nx>=len_maze or ny<0 or ny>=len_maze:
                continue
            else:
                maze[nx][ny] = 
                queue.append([nx,ny])
                


    
#도착가능 1 불가능 0
#상 하 좌 우
dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

for c in range(10):
    maze = [list(map(int, input().rstrip())) for _ in range(16)]
    queue = deque()
    print(f"#{c+1} {bfs(maze)}")
    pass

