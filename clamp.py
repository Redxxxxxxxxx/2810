def clamp(x, lo, hi):
    if any(isinstance(v, bool) for v in (x, lo, hi)) or \
       not all(isinstance(v, (int, float)) for v in (x, lo, hi)):
        raise TypeError("numeric only")
    if lo > hi:
        raise ValueError("lo must be <= hi")
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x