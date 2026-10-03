import sys
input = sys.stdin.readline

n, m = map(int, input().split())

graph = []
for i in range(n):
    graph.append(list(map(int, input().rstrip())))

result = 0

def dfs(x, y):
    if x < 0 or x>= n or y<0 or y>=m:
        return False
    if graph[x][y] == 0:
        graph[x][y] = 1
        dfs(x-1, y)
        dfs(x+1, y)
        dfs(x, y-1)
        dfs(x, y+1)
        return True
    else:
        return False


for x in range(n):
    for y in range(m):
        if dfs(x,y) == True:
            result += 1

print(graph)
print(f"{result}")