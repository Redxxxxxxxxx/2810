import pytest
from Xpower.tier_rate import tier_rate_calc

#Typical
@pytest.mark.parametrize("usage_data,expected", [
    ([["2025-01-01", "10:00", "50"]], 50*0.20 + 10),                        # T1: Only Tier 1 (50 kWh)
    ([["2025-01-01", "10:00", "200"]], 100*0.20 + 100*0.30 + 10),           # T2: Tier 1 full (100) + Tier 2 (100)
    ([["2025-01-01", "10:00", "350"]], 100*0.20 + 200*0.30 + 50*0.40 + 10), # T3: Tier 1 (100) + Tier 2 (200) + Tier 3 (50)
])
def test_tier_rate_typical_cases(usage_data, expected):
    result = tier_rate_calc(usage_data)
    assert result == expected

#Boundary
@pytest.mark.parametrize("usage_data,expected", [
    ([["2025-01-01", "10:00", "100"]], 100*0.20 + 10),              # B1: Exactly 100 kWh (boundary between Tier 1 and 2)
    ([["2025-01-01", "10:00", "300"]], 100*0.20 + 200*0.30 + 10),   # B2: Exactly 300 kWh (boundary between Tier 2 and 3)
    ([["2025-01-01", "10:00", "0"]], 10),                           # B3: Zero usage (bill = fixed fee only)
    ([["2025-01-01", "10:00", "-50"]], 10),                         # B4: Negative usage (ignored → bill = fixed fee only)
])
def test_tier_rate_boundary_cases(usage_data, expected):
    result = tier_rate_calc(usage_data)
    assert result == expected

#Invalid Cases
def test_I1_invalid_t1_rate_zero():
    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(ValueError) as e:
        tier_rate_calc(usage_data, t1_rate=0)
    assert "Tier 1 rate cannot be" in str(e.value)


def test_I2_invalid_t2_rate_zero():
    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(ValueError) as e:
        tier_rate_calc(usage_data, t2_rate=0)
    assert "Tier 2 rate cannot be" in str(e.value)


def test_I3_invalid_t3_rate_zero():
    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(ValueError) as e:
        tier_rate_calc(usage_data, t3_rate=0)
    assert "Tier 3 rate cannot be" in str(e.value)


def test_I4_invalid_fixed_fee_zero():
    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(ValueError) as e:
        tier_rate_calc(usage_data, fixed_fee=0)
    assert "Fixed fee cannot be" in str(e.value)


def test_I5_invalid_kwh_string():
    usage_data = [["2025-01-01", "10:00", "abc"]]
    with pytest.raises(ValueError):
        tier_rate_calc(usage_data)


def test_I6_invalid_rate_type():
    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(TypeError):
        tier_rate_calc(usage_data, t1_rate="bad")
