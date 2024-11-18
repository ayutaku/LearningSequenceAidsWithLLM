```
n = int(input())
ans = ''
i = 1
while i <= n:
    x = i
    if (x % 3) == 0:
        ans += ' ' + str(i)
        i += 1
    elif (x % 10) == 3:
        ans += ' ' + str(i)
        i += 1
    else:
        while True:
            x = (x // 10)
            if x == 0:
                i += 1
                break
            elif (x % 10) == 3:
                ans += ' ' + str(i)
                i += 1
                break
print(ans)
```