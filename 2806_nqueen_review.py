#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV7GKs06AU0DFAXB&categoryId=AV7GKs06AU0DFAXB&categoryType=CODE&problemTitle=queen&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1
# 리뷰할 때 실 수 했던 점은 N이 마지막에 어떻게 걸리는지 그리고 
# 마지막 종결조건에 대한 return 처리는 함수 시작단에 걸어주어야 좋다는 것.

import sys
input = sys.stdin.readline

def dfs(N,row): #매 col을 같이 받게 되는 것임 변수는 N은 사이즈, col
    global iscolused, isusedsum, isusedminus
    if row == N:
        return 1
    count = 0
    for col in range(N):
        j_sum, j_minus = col + row, N - row + col -1
        if iscolused[col] or isusedsum[j_sum] or isusedminus[j_minus]:
            continue
        iscolused[col] = isusedsum[j_sum] = isusedminus[j_minus] = True
        count += dfs(N,row=row+1)
        iscolused[col] = isusedsum[j_sum] = isusedminus[j_minus] = False
    return count

tc = int(input().rstrip())

#N은 정사각형 체스판 크기
for x in range(tc):
    N = int(input().rstrip())
    iscolused = [False] * N
    isusedsum = [False] * (2 * N - 1)
    isusedminus = [False] * (2 * N - 1)
    print(f"#{x+1} {dfs(N, 0)}")