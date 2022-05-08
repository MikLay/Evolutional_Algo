from helpers import grey_to_dec


def f_const_perfect_sequence(seq):
    return (seq == ("0" * len(seq))) or (seq == ("1" * len(seq)))


def fh_perfect_sequence(seq):
    return seq == ("0" * len(seq))


def perfect_sequence_1023(seq):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    # todo try to increase accuracy
    return 10.21 <= x <= 10.25


def perfect_sequence_0(seq):
    a = -5.11
    b = 5.12
    x = grey_to_dec(seq, a, b)
    # todo try to increase accuracy
    return -0.02 <= x <= 0.02