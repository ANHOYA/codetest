#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV7GKs06AU0DFAXB&categoryId=AV7GKs06AU0DFAXB&categoryType=CODE&problemTitle=queen&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

import sys
input = sys.stdin.readline

def dfs(N, row_cnt):
    if row_cnt == N:
        return 1  # 모든 행에 퀸을 놓았으므로 유효한 배치 한 가지를 반환
    case = 0
    for col in range(N):
        sum_idx = row_cnt + col  # 현재 칸의 오른쪽 아래 방향 대각선 인덱스
        minus_idx = row_cnt - col + N - 1  # 인덱스를 음수 없이 쓰도록 N-1만큼 이동

        if not iscolused[col] and not isusedsum[sum_idx] and not isusedminus[minus_idx]:
            iscolused[col] = isusedsum[sum_idx] = isusedminus[minus_idx] = True
            case += dfs(N, row_cnt=row_cnt + 1)  # 다음 행의 경우의 수를 현재 합계에 누적
            iscolused[col] = False  # 재귀에서 돌아오면 표시를 되돌려 다른 배치를 탐색
            isusedsum[sum_idx] = False
            isusedminus[minus_idx] = False

    return case

tc = int(input().rstrip())

for x in range(tc):
    N = int(input().rstrip())
    iscolused = [False] * N
    isusedsum = [False] * (2 * N - 1)
    isusedminus = [False] * (2 * N - 1)
    print(f"#{x+1} {dfs(N, 0)}")