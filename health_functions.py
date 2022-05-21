from math import exp

from helpers import grey_to_dec


def fconst(seq):
    """
    Fconst(X) визначена на ланцюжках виду «00…0» та «11…1», причому Fconst(«00…0»)=Fconst(«11…1»)=l=100;
    [Функція використовується тільки для дослідження ШУМУ відбору]
    """
    if (seq == "1" * len(seq)) or (seq == "0" * len(seq)):
        return len(seq)
    return 0


def fh(seq):
    """
    FH(X)=l-H(X,X_opt), де H(X,X_opt) – відстань Геммінга до оптимального ланцюжка Xopt=«0...0»
    (фактично кількість «0» в ланцюжку);
    """
    return len(list(filter(lambda i: i == '0', seq)))


def fhd(seq, q=10):
    """
    FHD(X)=(l-k)+k*δ – відстань до оптимального ланцюжка Xopt=«0...0» з врахуванням селективної переваги
    на біт (параметр δ), де k – кількість «0» в ланцюжку; очевидно, FHD(«0...0»)=l*δ.
    Розглянути такі значення селективної переваги:  δ=10, δ=50, δ=150. ( δ=2, δ=4,  δ=10)

    # todo ask if k is number of 0 or 1
    """
    l = len(seq)
    k = len(list(filter(lambda i: i == '0', seq)))
    return (l-k) + k * q


def fhd_10(seq):
    return fhd(seq)


def fhd_50(seq):
    return fhd(seq, 50)


def fhd_150(seq):
    return fhd(seq, 150)


def grey_x_2(seq):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    return x ** 2


def grey_x(seq):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    return x


def grey_x_4(seq):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    return x ** 4


def grey_2_x_2(seq):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    return 2 * x ** 2


def grey_512_x_2(seq):
    a = -5.11
    b = 5.12
    x = grey_to_dec(seq, a, b)
    return (5.12 ** 2) - (x ** 2)


def grey_512_x_4(seq):
    a = -5.11
    b = 5.12
    x = grey_to_dec(seq, a, b)
    return (5.12 ** 4) - (x ** 4)


def grey_e_x_c(seq, c):
    a = 0
    b = 10.23
    x = grey_to_dec(seq, a, b)
    return exp(c * x)


def grey_e_x_025(seq):
    return grey_e_x_c(seq, 0.25)


def grey_e_x_1(seq):
    return grey_e_x_c(seq, 1)


def grey_e_x_2(seq):
    return grey_e_x_c(seq, 2)

# ---------------------------


def grey_x_2_get_x_by_y(y):
    return [y ** 0.5]


def grey_x_get_x_by_y(y):
    return [y]


def grey_x_4_get_x_by_y(y):
    return [y ** 0.25]


def grey_512_x_2_get_x_by_y(y):
    r = round((5.12 ** 2 - y) ** 0.5, 2)
    return [-r, r]


def grey_512_x_4_get_x_by_y(y):
    r = round((5.12 ** 4 - y) ** 0.25, 2)
    return [-r, r]
