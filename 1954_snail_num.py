#https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5PobmqAPoDFAUq#none

#vector 처리기
class vertor_status:
    def __init__(self):
        self.value = int(0)
    
    def __call__(self):
        return self.value

    def next(self):
        if self.value <3:
            self.value += 1
        else:
            self.value = 0

#T case 입력
T = int(input())

for j in range(T):
    #2차원 배열 선언
    N = int(input())
    array = [[0] * N for _ in range(N)]
    len_array = len(array)

    #움직이는 방향 선언
    vector = [[0,1],[1,0],[0,-1],[-1,0]]
    vec_status = vertor_status()
    cursor = [0,0]
    for i in range(N*N):
        array[cursor[0]][cursor[1]] = i + 1
        local_vec = vector[vec_status()]
        try:
            if array[cursor[0]+local_vec[0]][cursor[1]+local_vec[1]] != 0:
                vec_status.next()
        except:
            vec_status.next()
        local_vec = vector[vec_status()]
        
        cursor[0] += local_vec[0]
        cursor[1] += local_vec[1]

    print(f"#{j+1}")

    for i in array :
        for j in i:
            print(j,end=" ")
        print()