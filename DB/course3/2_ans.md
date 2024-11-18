```
import sys
read = sys.stdin.buffer.read
readline = sys.stdin.buffer.readline
readlines = sys.stdin.buffer.readlines
sys.setrecursionlimit(500000)

while True:
    n, x = map(int, readline().split())
    if (n + x) == 0:
        break
    cnt = 0
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            for c in range(b + 1, n + 1):
                if a + b + c == x:
                    cnt += 1
    print(cnt)
```