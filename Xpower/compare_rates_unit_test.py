import pytest
from Xpower.function_4_compare_rates import compare_rates


#Typical
def test_T1_compare_rates_typical_case(capsys):
    usage_data = [
        ["2025-01-01", "10:00", "50"],   # Shoulder
        ["2025-01-01", "02:00", "50"],   # Off-peak
        ["2025-01-01", "19:00", "50"],   # Peak
    ]
    compare_rates(usage_data)
    captured = capsys.readouterr()

    # Should print all three plan costs
    assert "Your Flat Rate Plan Cost Will Be" in captured.out
    assert "Your Time Rate Plan Cost Will Be" in captured.out
    assert "Your Tier Rate Plan Cost Will Be" in captured.out

    # Should print cheapest plan line
    assert "Your Cheapest Plan Will Be" in captured.out


#Boundary
def test_B1_compare_rates_equal_costs(capsys):
    # Zero usage - Fixed fee only
    usage_data = [
        ["2025-01-01", "10:00", "0"],
        ["2025-01-01", "19:00", "0"],
    ]
    compare_rates(usage_data)
    captured = capsys.readouterr()

    # Should still print all costs and cheapest as first one encountered
    assert "Flat Rate" in captured.out
    assert "Time Rate" in captured.out
    assert "Tier Rate" in captured.out
    assert "Your Cheapest Plan Will Be Flat Rate" in captured.out


#Invalid
def test_I1_compare_rates_error_zero_fee(monkeypatch):
    import Xpower.function_4_compare_rates as compare_mod
    monkeypatch.setattr(compare_mod, "flat_rate_calc", lambda data, **kwargs: 0)

    usage_data = [["2025-01-01", "10:00", "100"]]
    with pytest.raises(ValueError) as e:
        compare_mod.compare_rates(usage_data)
    assert "Error, Fee Cannot Be $0.00" in str(e.value)



def test_I2_compare_rates_invalid_input_type():
    # Bad input: string kWh should bubble up from underlying calculators
    usage_data = [["2025-01-01", "10:00", "abc"]]
    with pytest.raises(ValueError):
        compare_rates(usage_data)
