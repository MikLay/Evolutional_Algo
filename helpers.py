def gray_to_int(n):
    n = int(n, 2)  # convert to int
    mask = n
    while mask != 0:
        mask >>= 1
        n ^= mask
    return n


def grey_to_dec(seq, a, b):
    n = gray_to_int(seq)
    m = len(seq)
    return a + n * (b - a)/(2 ** m - 1)

def binary_to_gray(n):
    n ^= (n >> 1)

    # bin(n) returns n's binary representation with a '0b' prefixed
    # the slice operation is to remove the prefix
    return bin(n)[2:]

def dec_to_grey(x, a, b):
    m = 10
    n = int((x - a) * (2 ** m - 1) / (b - a))
    return binary_to_gray(n)