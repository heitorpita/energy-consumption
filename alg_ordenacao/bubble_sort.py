n = int(input())
v = list(map(int, input().split()))

for i in range(n - 1):
    for j in range(n - 1):
        if v[j] > v[j + 1]:
            v[j], v[j + 1] = v[j + 1], v[j]

print(n)
print(" ".join(map(str, v)))
