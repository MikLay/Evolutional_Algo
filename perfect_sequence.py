def f_const_perfect_sequence(seq):
    return (seq == ("0" * len(seq))) or (seq == ("1" * len(seq)))


def fh_perfect_sequence(seq):
    return seq == ("0" * len(seq))