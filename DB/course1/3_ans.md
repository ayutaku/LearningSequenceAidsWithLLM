```
while True:
    H, W = map(int,input().split())
    if H == W == 0:
        break
    for h in range(H):
        tmp = ''
        for w in range(W):
            tmp += "#" if (h + w) % 2 == 0 else '.'
        print(tmp)
    print()
```