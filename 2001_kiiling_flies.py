#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5PzOCKAigDFAUq&categoryId=AV5PzOCKAigDFAUq&categoryType=CODE&problemTitle=2001&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=1

class array:
    def __init__(self, N):
        self.N = N
        self.ego_array = [[0] * N for _ in range(N)]
        for j in range(N):
            self.ego_array[j] = list(map(int, input().split()))

    def __call__(self, *args, **kwds):
        return self.ego_array

    def kill_flies(self, M):
        arr = self.ego_array
        total_kills = 0 
        cnt_iter_filter = len(arr)-M+1
        for i in range(cnt_iter_filter):#row
            for j in range(cnt_iter_filter):#col
                local_kills = 0
                for row_arr in arr[i:i+M]:
                    local_kills += sum(row_arr[j:j+M])
                if local_kills >= total_kills:
                    total_kills = local_kills
        return total_kills

tc = int(input())

for i in range(tc):
    N, M = map(int, input().split())
    make_array = array(N)
    print(f"#{i+1} {make_array.kill_flies(M)}")