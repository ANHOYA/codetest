#https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/royal-knight-duel/description
import sys
input = sys.stdin.readline

#상하좌우 def 0,1,2,3 위 오른쪽 아래 왼쪽
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

def move(i,d): 
    global knights_damage, knights, chessboard, dr, dc
    #기사 움직이고 / 움직이면서 벽 체크 and 움직임 가능 체크 / 움직이면서 체력 깍기
    #i 번째 기사, d방향으로 한 칸 이동 | knight row 범위 [[r1,r2], [c1,c2]]
    # knights 맨 앞 번호 0번째는 안 쓰도록 잘 처리.
    #0 빈칸 / 1 함정 / 2 벽
    #재귀적으로 옆이 벽인지 호출해서 확인 하는 코드
    nr = [knights[i][0]+dr[d], knights[i][1]+dr[d]]
    nc = [knights[i][2]+dc[d], knights[i][3]+dc[d]]
    for r in nr:
        for c in nc:
            if (type(chessboard[r][c]) == bool) or chessboard[r][c] == 2:
                return False
    
    for k_idx, each_knight in enumerate(knights):
        if k_idx == i or k_idx==0 or (each_knight[4]==0):
            continue
        judge = []
        for r in nr:
            for c in nc:
                judge.append((each_knight[0] <= r and each_knight[1] >= r) and (each_knight[2] <= c and each_knight[3] >= c)) #모두 True이면 따라서 움직이는 애가 필요
        if (True in judge):
            temp = move(k_idx,d)
            if temp == False:
                continue
            # knights[i] = [nr[0], nr[1], nc[0], nc[1], each_knight[-1]]
            update_knights(i, [nr[0], nr[1], nc[0], nc[1], each_knight[-1]])

            #괜찮다고 하면.
            for r in knights[i][0:2]:
                for c in knights[i][2:4]:
                    if chessboard[r][c] == 1:
                        knights[i][4] -= 1
                        if knights[i][4] == 0:
                            knights[i] = [0,0,0,0,0]
            # knights[i] = [knights[i][0]+dr[d], knights[i][1]+dr[d], knights[i][2]+dc[d], knights[i][3]+dc[d], knights[i][4]]
            return True

def update_knights(i, content):
    global knights
    knights[i] = content

#L, N, Q
L, N, Q = map(int, input().split())

#L x L 체스판 좌상단 (1,1)
chessboard = []
for i in range(L+2):
    if i ==0 or i==L+1:
        chessboard.append([[True]*(L+2)])
    else: #0빈칸 1함정 2벽
        chessboard.append([True] + list(map(int, input().split())) + [True])

#N개의 기사 정보 (r,c,h,w,k) / k는 체력
knights_info = [[]]
for i in range(N):
    knights_info.append(list(map(int, input().split())))
knights = [[]]

for each_knight in knights_info: #knight row 범위 [r1,r2, c1,c2, k]
    if each_knight == []:
        continue
    knights.append([each_knight[0], each_knight[0]+each_knight[2]-1, each_knight[1],each_knight[1]+each_knight[3]-1, each_knight[4]])

#Q번의 명령
knights_damage = [0]*(N+1)
for _ in range(Q):
    i, d = map(int, input().split()) #i 번째 기사, d방향으로 한 칸 이동
    move(i,d)

#최종 출력 "생존한" 기사들이 받은 데미지의 총합
result = 0
for k in knights:
    result += k[4]
print(result, knights)