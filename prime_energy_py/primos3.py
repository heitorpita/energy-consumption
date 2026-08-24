import sys
import math


def is_prime_sqrt(n):

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = math.isqrt(n)
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Numero: "))
    if n < 0:
        print(n, "é negativo")
    elif n == 0:
        print(n, "é zero")
    elif is_prime_sqrt(n):
        print(n, "é primo")
    else:
        print(n, "não é primo")