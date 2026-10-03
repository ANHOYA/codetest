import sys, math
input = sys.stdin.readline

S = list(map(int, input().rstrip()))
S.append(1)
result = 0
temp = []
for x in S:
    if x == 0 or x==1:
        if len(temp) != 0:
            result += math.prod(temp)
            temp = []
        result += x
    else:
        temp.append(x)

print(result-1)