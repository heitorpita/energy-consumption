n = int(input())
v = list(map(int, input().split()))

limite = n - 1
while limite > 0:
    ultima = 0
    for j in range(limite):
        if v[j] > v[j + 1]:
            v[j], v[j + 1] = v[j + 1], v[j]
            ultima = j
    limite = ultima

print(n)
print(" ".join(map(str, v)))
