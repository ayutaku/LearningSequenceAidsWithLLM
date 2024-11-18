```
info = [int(i) for i in input().rstrip().split()]
n = info[0]
m = info[1]
l = info[2]

matrixA = []
matrixB = []
for i in range(n):
    row = [int(j) for j in input().rstrip().split()]
    matrixA.append(row)
for j in range(m):
    row = [int(k) for k in input().rstrip().split()]
    matrixB.append(row)

for i in range(n):
    multipleRow = []
    for k in range(l):
        total = 0
        for j in range(m):
            total += matrixA[i][j] * matrixB[j][k]
        multipleRow.append(str(total))
    print(' '.join(multipleRow))
```