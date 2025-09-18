
import pytest
from clamp import clamp

# ---------------- Typical (T1..T5) ----------------
@pytest.mark.parametrize("x,lo,hi,expected", [
    (5, 0, 10, 5),             # T1 Inside range -> x
    (-2, -5, 5, -2),           # T2 Inside negative range -> x
    (12.5, 0.0, 20.0, 12.5),   # T3 Float inside range -> x
])
def test_typical_cases(x, lo, hi, expected):
    assert clamp(x, lo, hi) == expected

# ---------------- Boundary (B1..B9) ----------------
@pytest.mark.parametrize("x,lo,hi,expected", [
    (9, 10, 20, 10),       # B1 just below lower -> lo
    (10, 10, 20, 10),      # B2 exactly lower -> x
    (11, 10, 20, 11),      # B3 just above lower -> x
    (19, 10, 20, 19),      # B4 just below upper -> x
    (20, 10, 20, 20),      # B5 exactly upper -> x
    (21, 10, 20, 20),      # B6 just above upper -> hi
    (7, 7, 7, 7),          # B7 equality edge lo==hi -> x
    (6.9999, 7, 7, 7),     # B8 just below equality edge -> clamp to lo(=hi)
    (7.0001, 7, 7, 7),     # B9 just above equality edge -> clamp to hi(=lo)
])
def test_boundary_cases(x, lo, hi, expected):
    assert clamp(x, lo, hi) == expected

# ---------------- Invalid (I1..I7) ----------------

def test_I1_invalid_range_order_valueerror():
    with pytest.raises(ValueError) as e:
        clamp(0, 10, 5)
    assert "lo must be <=" in str(e.value)

@pytest.mark.parametrize("args", [
    (("5", 0, 10)),   # I2 Non-numeric x
    ((5, "0", 10)),   # I3 Non-numeric lo
    ((5, 0, "10")),   # I4 Non-numeric hi
    ((True, 0, 10)),  # I5 Bool x not allowed
    ((5, False, 10)), # I6 Bool lo not allowed
    ((5, 0, True)),   # I7 Bool hi not allowed
])
def test_invalid_typeerror_and_message(args):
    with pytest.raises(TypeError) as e:
        clamp(*args)
    assert "numeric only" in str(e.value)
