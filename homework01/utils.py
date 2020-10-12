def shifting(ord_numb: int, shift: int, bound1: int = ord("A"), bound2: int = ord("Z")) -> int:
    """
    Changes char according to its order and given shift value.
    """
    ord_numb += shift
    if ord_numb > bound2:
        ord_numb -= bound2 - bound1 + 1
    elif ord_numb < bound1:
        ord_numb += bound2 - bound1 + 1
    return ord_numb
