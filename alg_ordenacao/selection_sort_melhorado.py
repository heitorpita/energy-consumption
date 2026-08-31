n = int(input())
v = list(map(int, input().split()))

ini = 0
fim = n - 1
while ini < fim:
    imin = ini
    imax = ini
    for k in range(ini + 1, fim + 1):
        if v[k] < v[imin]:
            imin = k
        elif v[k] > v[imax]:
            imax = k
    if imin != ini:
        v[ini], v[imin] = v[imin], v[ini]
        if imax == ini:
            imax = imin
    if imax != fim:
        v[fim], v[imax] = v[imax], v[fim]
    ini += 1
    fim -= 1

print(n)
print(" ".join(map(str, v)))
