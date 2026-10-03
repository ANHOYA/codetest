tc = int(input())

for case in range(1, tc + 1):
    N, M = map(int, input().split())
    flies = [list(map(int, input().split())) for _ in range(N)]

    prefix = [[0] * (N + 1) for _ in range(N + 1)]
    for row in range(N):
        for col in range(N):
            prefix[row + 1][col + 1] = (
                flies[row][col]
                + prefix[row][col + 1]
                + prefix[row + 1][col]
                - prefix[row][col]
            )

    max_kills = 0
    for row in range(N - M + 1):
        for col in range(N - M + 1):
            kills = (
                prefix[row + M][col + M]
                - prefix[row][col + M]
                - prefix[row + M][col]
                + prefix[row][col]
            )
            max_kills = max(max_kills, kills)

    print(f"#{case} {max_kills}")
