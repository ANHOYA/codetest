#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV7GKs06AU0DFAXB&categoryId=AV7GKs06AU0DFAXB&categoryType=CODE&problemTitle=queen&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys
input = sys.stdin.readline

def dfs(N, row_cnt):
    case = 0
    if N == row_cnt:
        return 1
    for col in range(N):
        idx_diag = row_cnt+col
        idx_revdiag = row_cnt-col+N-1
        if not (iscolused[col] or isdiagonalused[idx_diag] or isreversediagonalused[idx_revdiag]): #하나라도 True이면 차있으면,,,
            iscolused[col] = isreversediagonalused[idx_revdiag] = isdiagonalused[idx_diag] = True
            case += dfs(N, row_cnt=row_cnt+1)
            iscolused[col] = isreversediagonalused[idx_revdiag] = isdiagonalused[idx_diag] = False
    return case

tc = int(input().rstrip())
for i in range(tc):
    N = int(input().rstrip())
    iscolused = [False] * N
    isdiagonalused = [False] * (2*N-1)
    isreversediagonalused = [False] * (2*N-1)
    print(f"#{i+1} {dfs(N,0)}")