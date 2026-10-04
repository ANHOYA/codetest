import sys, math
input = sys.stdin.readline

S = list(map(int, input().rstrip()))
S.append(1)
result = 0 #처음 숫자를 애초부터 S[0]으로 잡는 거이 더 편하네
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