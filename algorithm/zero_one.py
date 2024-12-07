N=3
CC=6

W = [0,2,3,4]
V = [0,3,5,6]

matrix = [[0 for x in range(CC+1)] for y in range(N+1)]

print(matrix)

for i in range(1, N+1):
    for j in range(1, CC+1):
        if j < W[i]:
            matrix[i][j] = matrix[i-1][j]
        else:
            data1 = matrix[i-1][j]
            data2 = matrix[i-1][j-W[i]] + V[i]
            matrix[i][j] = max(data1, data2)
print(matrix)
