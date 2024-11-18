'''
r, c = map(int, input().split())
goukei = [0]*c
for i in range(r):
    tmp = list(map(int, input().split()))
    for j in range(c):
        goukei[j] += tmp[j]
    print(' '.join(map(str, tmp)) + ' ' + str(sum(tmp)))
print(' '.join(map(str, goukei)) + ' ' + str(sum(goukei)))
'''