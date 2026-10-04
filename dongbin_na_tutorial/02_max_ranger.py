import sys
input = sys.stdin.readline

N = int(input().rstrip())
rangers = list(map(int, input().split()))

rangers.sort()
max_capacity = rangers[0]
man_queue = 0
result = 0
for idx, man in enumerate(rangers):
    man_queue += 1
    if man > max_capacity:
        max_capacity = man
        continue
    if max_capacity == man_queue:
        result += 1
        man_queue = 0
        if idx < len(rangers)-1:
            max_capacity = rangers[idx+1]

print(result)