```
while True:
    m,f,r = list(map(float,input().split()))
    if m==-1 and f==-1 and r==-1:
        break
    else:
        if f==-1 or m==-1:
            print("F")
        elif m+f<30:
            print("F")
        elif 30<=m+f<50:
            if 50<=r:
                print("C")
            else:
                print("D")
        elif 50<=m+f<65:
            print("C")
        elif 65<=m+f<80:
            print("B")
        elif 80<=m+f:
            print("A")
```