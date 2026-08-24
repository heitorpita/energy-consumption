import sys


def is_prime_naive(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Numero: "))
    if n < 0:
        print(n, "é negativo")
    elif n == 0:
        print(n, "é zero")
    elif is_prime_naive(n):
        print(n, "é primo")
    else:
        print(n, "não é primo")