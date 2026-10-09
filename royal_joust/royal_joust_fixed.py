"""왕실의 기사 대결: 원본의 동작을 주석으로 짚으며 고친 풀이."""

import sys
from collections import deque

input = sys.stdin.readline

# 0: 위, 1: 오른쪽, 2: 아래, 3: 왼쪽
dr = (-1, 0, 1, 0)
dc = (0, 1, 0, -1)


def overlap(a, b):
    """[위, 아래, 왼쪽, 오른쪽, 체력] 형태인 두 기사가 겹치는지 확인."""
    return not (a[1] < b[0] or b[1] < a[0] or a[3] < b[2] or b[3] < a[2])

def move(start, direction):
    if knights[start][4] <= 0:
        return

    # 첨삭: knights는 전역 리스트이므로 knights[i] = ... 자체는 전역에 반영된다.
    # 원본의 핵심 문제는 로컬/글로벌이 아니라 재귀 도중 상태를 먼저 바꾸는 순서다.
    # 밀리는 기사 중 하나라도 벽에 막히면 이미 움직인 기사까지 취소해야 하므로,
    # 먼저 이동 대상과 벽 여부를 모두 확인하고, 성공할 때만 한 번에 갱신한다.
    moving = {start}
    queue = deque([start])

    while queue:
        i = queue.popleft()
        top, bottom, left, right, _ = knights[i]
        next_top = top + dr[direction]
        next_bottom = bottom + dr[direction]
        next_left = left + dc[direction]
        next_right = right + dc[direction]

        # 첨삭: 원본은 밀린 기사의 이동이 실패해도 `continue`로 넘겨 버린다.
        # 한 기사라도 막히면 명령 전체가 실패해야 하므로 여기서 즉시 종료한다.
        # 또 원본의 `for r in nr: for c in nc:`는 네 모서리만 검사한다.
        # 직사각형의 변 가운데에 벽이 있을 수도 있으므로 새 영역 전체를 검사한다.
        for r in range(next_top, next_bottom + 1):
            for c in range(next_left, next_right + 1):
                if board[r][c] == 2:
                    return

        next_rect = [next_top, next_bottom, next_left, next_right, 0]
        for other in range(1, n + 1):
            if other in moving or knights[other][4] <= 0:
                continue
            if overlap(next_rect, knights[other]):
                moving.add(other)
                queue.append(other)

    # 첨삭: 원본은 다른 기사와 부딪힐 때만 이동한다. 단독 이동도 여기서 처리한다.
    for i in moving:
        knights[i][0] += dr[direction]
        knights[i][1] += dr[direction]
        knights[i][2] += dc[direction]
        knights[i][3] += dc[direction]

    for i in moving:
        if i == start:
            continue  # 첨삭: 명령받은 기사는 이번 이동에서 함정 피해를 받지 않는다.

        top, bottom, left, right, _ = knights[i]
        traps = sum(
            board[r][c] == 1
            for r in range(top, bottom + 1)
            for c in range(left, right + 1)
        )
        # 첨삭: 원본의 each_knight[-1]은 밀려나는 다른 기사의 체력이다.
        # 각 기사의 체력은 자기 값에서 함정 수만큼만 차감한다.
        knights[i][4] -= traps


l, n, q = map(int, input().split())

# 첨삭: 원본의 위/아래 테두리는 [[True] * ...]여서 행 크기가 1이며,
# 좌우 테두리의 True도 정수 1(함정)처럼 취급될 수 있다. 벽(2)으로 통일한다.
board = [[2] * (l + 2)]
for _ in range(l):
    board.append([2] + list(map(int, input().split())) + [2])
board.append([2] * (l + 2))

knights = [[]]
initial_hp = [0]
for _ in range(n):
    r, c, h, w, hp = map(int, input().split())
    knights.append([r, r + h - 1, c, c + w - 1, hp])
    initial_hp.append(hp)

for _ in range(q):
    i, d = map(int, input().split())
    move(i, d)

# 첨삭: 원본은 빈 0번 기사([])까지 순회해서 k[4]에서 오류가 난다.
# 요구하는 값은 생존 기사의 남은 체력 합이 아니라 받은 피해 합이다.
print(sum(initial_hp[i] - knights[i][4] for i in range(1, n + 1) if knights[i][4] > 0))
