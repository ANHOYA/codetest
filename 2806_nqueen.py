#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV7GKs06AU0DFAXB&categoryId=AV7GKs06AU0DFAXB&categoryType=CODE&problemTitle=queen&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys
input = sys.stdin.readline

def dfs(N, row_cnt):
    case = 0
    for col in range(N):
        iscolused[col], isusedsum[col+row_cnt], isusedminus[col]


    return case

tc = input().rstrip()

for x in range(tc):
    N = int(input().rstrip())
    iscolused = [[False] * N for _ in range(N)]
    isusedsum = [[False] * (2 * N - 1) for _ in range(2 * N - 1)]
    isusedminus = [[False] * (2 * N - 1) for _ in range(2 * N - 1)]
    print(f"#{x} {dfs(N, 0)}")