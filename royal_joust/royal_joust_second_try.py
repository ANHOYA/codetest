#https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/royal-knight-duel/description
import sys
input = sys.stdin.readline

from collections import deque

#상하좌우 def 0,1,2,3 위 오른쪽 아래 왼쪽
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

def overlap(a,b): #(r,c,h,w,k)
    #겹친다의 정의가 더 작은 r에 h-1 합한 값이 나머지 더 큰 r값보다 크거나 같을 때, 이게 r,c and로 걸릴 때.
    if b[0]<a[0]:
        a,b = b,a
    r_lap = True if a[0]+a[2]-1 >= b[0] else False
    if b[1]<a[1]:
        a,b = b,a
    c_lap = True if a[1]+a[3]-1 >= b[1] else False
    return r_lap and c_lap  

def move(i, d): #i 기사 인덱스 | d 방향 인덱스
    pass
    queue = deque()
    queue.append(i) #기사 인덱스로 넣어. $$$$$$$$$$기사 불러올때, 피가 0이면 무시#$#$##$
    
    while queue:
        this_knight = queue.popleft()
        #기사 다음 위치 산출
        next_knight = [this_knight[0]+dr[i], this_knight[1]+dr[i], this_knight[2], this_knight[3], this_knight[4]]
        #밀어내는 것이 있는가? | 막히지는 않았는가? / 죽은 나이트는 어떻게 처리할 것인가?
        overlap_list = []
        knights

    #움직여도 된다면. moving queue에 대기

    #다 통과해서 valid하면 움직인다




#L, N, Q
L, N, Q = map(int, input().split())

#L x L 체스판 좌상단 (1,1)
board = []
for i in range(L+2):
    if i ==0 or i==L+1:
        board.append([[2]*(L+2)])
    else: #0빈칸 1함정 2벽 | 범위 바깥도 벽으로 통일해서 밖으로 나가지 못하게 구성
        board.append([2] + list(map(int, input().split())) + [2])

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