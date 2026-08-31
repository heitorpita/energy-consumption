n = int(input())
v = list(map(int, input().split()))

for i in range(n):
    menor = i
    for k in range(i + 1, n):
        if v[k] < v[menor]:
            menor = k
    v[i], v[menor] = v[menor], v[i]

print(n)
print(" ".join(map(str, v)))
