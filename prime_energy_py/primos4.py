import sys


def is_prime_6k(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Numero: "))
    if n < 0:
        print(n, "é negativo")
    elif n == 0:
        print(n, "é zero")
    elif is_prime_6k(n):
        print(n, "é primo")
    else:
        print(n, "não é primo")