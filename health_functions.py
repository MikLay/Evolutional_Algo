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