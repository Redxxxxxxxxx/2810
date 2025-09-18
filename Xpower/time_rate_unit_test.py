import pytest
from Xpower.time_of_use import time_rate_calc

#Typical
@pytest.mark.parametrize("usage_data,expected", [
    ([["2025-01-01", "19:00", "100"]], 100*0.40 + 10),                                              # T1 Peak usage only
    ([["2025-01-01", "02:00", "50"]], 50*0.15 + 10),                                                # T2 Off-peak usage only
    ([["2025-01-01", "10:00", "80"]], 80*0.25 + 10),                                                # T3 Shoulder usage only
    ([["2025-01-01", "02:00", "20"], ["2025-01-01", "12:00", "30"], ["2025-01-01", "19:00", "40"]], # T4 Mixed categories
     20*0.15 + 30*0.25 + 40*0.40 + 10),
])
def test_time_rate_typical_cases(usage_data, expected):
    result = time_rate_calc(usage_data)
    assert result == expected

#Boundary
@pytest.mark.parametrize("usage_data,expected", [
    ([["2025-01-01", "07:00", "10"]], 10*0.25 + 10),    # B1 Exactly at 07:00 → shoulder
    ([["2025-01-01", "18:00", "10"]], 10*0.40 + 10),    # B2 Exactly at 18:00 → peak
    ([["2025-01-01", "22:00", "10"]], 10*0.25 + 10),    # B3 Exactly at 22:00 → shoulder
    ([["2025-01-01", "10:00", "-100"]], 0*0.25 + 10),   # B4 Negative usage ignored
    ([["2025-01-01", "10:00", "0"]], 0*0.25 + 10),      # B5 Zero usage → only fixed fee
])
def test_time_rate_boundary_cases(usage_data, expected):
    result = time_rate_calc(usage_data)
    assert result == expected


#Invalid
def test_I1_invalid_peak_rate_zero():
    usage_data = [["2025-01-01", "19:00", "10"]]
    with pytest.raises(ValueError) as e:
        time_rate_calc(usage_data, peak_rate=0)
    assert "Peak rate cannot be" in str(e.value)


def test_I2_invalid_off_peak_rate_zero():
    usage_data = [["2025-01-01", "02:00", "10"]]
    with pytest.raises(ValueError) as e:
        time_rate_calc(usage_data, off_peak_rate=0)
    assert "Off-peak rate cannot be" in str(e.value)


def test_I3_invalid_shoulder_rate_zero():
    usage_data = [["2025-01-01", "10:00", "10"]]
    with pytest.raises(ValueError) as e:
        time_rate_calc(usage_data, shoulder_rate=0)
    assert "Shoulder rate cannot be" in str(e.value)


def test_I4_invalid_fixed_fee_zero():
    usage_data = [["2025-01-01", "10:00", "10"]]
    with pytest.raises(ValueError) as e:
        time_rate_calc(usage_data, fixed_fee=0)
    assert "Fixed fee cannot be" in str(e.value)


def test_I5_invalid_time_format():
    usage_data = [["2025-01-01", "25:00", "10"]]
    with pytest.raises(ValueError) as e:
        time_rate_calc(usage_data)
    assert "Invalid Time Period" in str(e.value)


def test_I6_invalid_kwh_string():
    usage_data = [["2025-01-01", "10:00", "abc"]]
    with pytest.raises(ValueError):
        time_rate_calc(usage_data)


def test_I7_invalid_rate_type():
    usage_data = [["2025-01-01", "10:00", "10"]]
    with pytest.raises(TypeError):
        time_rate_calc(usage_data, peak_rate="abc")
