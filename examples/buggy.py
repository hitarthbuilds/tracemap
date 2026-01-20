def divide(a, b):
    result = a / b
    return result


def pipeline(x):
    y = x - 1
    z = divide(x, y)
    return z


def main():
    value = 1
    output = pipeline(value)
    return output


main()
