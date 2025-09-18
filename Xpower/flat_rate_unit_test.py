import pytest
from Xpower.flat_rate import flat_rate_calc

#Valid
@pytest.mark.parametrize("usage_data,rate,fee,expected", [
    ([["2025-01-01", "12:00", "100"], ["2025-01-02", "12:00", "200"]], 0.25, 10, 85.0), # T1 Normal usage
    ([["2025-01-01", "12:00", "100"], ["2025-01-02", "12:00", "-50"]], 0.25, 10, 35.0), # T2 Mixed positive & negative (negative ignored)
])
def test_flat_rate_typical_cases(usage_data, rate, fee, expected):
    assert flat_rate_calc(usage_data, rate, fee) == expected

#Boundary
@pytest.mark.parametrize("usage_data,rate,fee,expected", [
    ([["2025-01-01", "12:00", "0"], ["2025-01-02", "12:00", "0"]], 0.25, 10, 10.0),      # B1 Zero usage only fixed fee
    ([["2025-01-01", "12:00", "-100"], ["2025-01-02", "12:00", "-50"]], 0.25, 10, 10.0), # B2 All negative usage ignored, only fixed fee
])
def test_flat_rate_boundary_cases(usage_data, rate, fee, expected):
    assert flat_rate_calc(usage_data, rate, fee) == expected


#Invalid
def test_flat_rate_invalid_zero_rate():
    usage_data = [["2025-01-01", "12:00", "100"]]
    with pytest.raises(ValueError) as e:
        flat_rate_calc(usage_data, flat_rate=0.0, fixed_fee=10)
    assert "Flat rate cannot be" in str(e.value)

def test_flat_rate_invalid_zero_fee():
    usage_data = [["2025-01-01", "12:00", "100"]]
    with pytest.raises(ValueError) as e:
        flat_rate_calc(usage_data, flat_rate=0.25, fixed_fee=0.0)
    assert "Fixed fee cannot be" in str(e.value)

def test_I3_invalid_kwh_string():
    usage_data = [["2025-01-01", "12:00", "abc"]]
    with pytest.raises(ValueError):  # float("abc") raises ValueError
        flat_rate_calc(usage_data, flat_rate=0.25, fixed_fee=10)


def test_I4_invalid_flat_rate_string():
    usage_data = [["2025-01-01", "12:00", "100"]]
    with pytest.raises(TypeError):
        flat_rate_calc(usage_data, flat_rate="abc", fixed_fee=10)


def test_I5_invalid_fixed_fee_string():
    usage_data = [["2025-01-01", "12:00", "100"]]
    with pytest.raises(TypeError):
        flat_rate_calc(usage_data, flat_rate=0.25, fixed_fee="xyz")