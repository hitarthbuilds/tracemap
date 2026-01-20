def expensive_loop(n):
    total = 0
    for i in range(n):
        total += i
    return total


def cheap_wrapper():
    result = expensive_loop(5_000_000)
    return result


def main():
    return cheap_wrapper()


main()
