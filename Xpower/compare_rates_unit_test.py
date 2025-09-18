import pytest
from Xpower.compare_rates import compare_rates


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

    #Should print cheapest plan line
    assert "Your Cheapest Plan Will Be" in captured.out


#Boundary
def test_B1_compare_rates_equal_costs(capsys):
    #Zero usage Fixed fee only
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
def test_I1_compare_rates_invalid_kwh_string():
    usage_data = [["2025-01-01", "10:00", "abc"]]  #str kWh
    with pytest.raises(ValueError):
        compare_rates(usage_data)


def test_I2_compare_rates_negative_kwh(capsys):
    usage_data = [["2025-01-01", "10:00", "-50"]]
    compare_rates(usage_data)   # just run it
    captured = capsys.readouterr()
    assert "Your Cheapest Plan Will Be Flat Rate With A Cost Of: $10.0" in captured.out


def test_I3_compare_rates_invalid_time_format():
    usage_data = [["2025-01-01", "25:00", "10"]]
    with pytest.raises(ValueError):
        compare_rates(usage_data)
