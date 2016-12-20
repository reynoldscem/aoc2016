import math
def main():
    init_circle_len = 3001330
    exponent = 3**int(math.log(init_circle_len, 3))

    if init_circle_len == exponent:
        res = exponent
    elif init_circle_len - exponent <= exponent:
        res = init_circle_len - exponent
    else:
        res = abs(2*init_circle_len - 3 * exponent)

    print(init_circle_len, res)

if __name__ == '__main__':
    main()
