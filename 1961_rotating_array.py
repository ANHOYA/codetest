#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5Pq-OKAVYDFAUq

def zero_array(N):
    return [[0] * N for _ in range(N)]

import sys
input = sys.stdin.readline

tc = int(input())

for i in range(tc):
    N = int(input())
    array = zero_array(N)
    for j in range(N):
        array[j] = list(map(int, input().split()))
    array_90 = list(map(list, zip(*array[::-1])))
    array_180 = list(map(list, zip(*array_90[::-1])))
    array_270 = list(map(list, zip(*array_180[::-1])))

    print(f"#{i+1}")
    for k in range(N):
        print(
            ''.join(map(str, array_90[k])),
            ''.join(map(str, array_180[k])),
            ''.join(map(str, array_270[k]))
)

    