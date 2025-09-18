#Tier Based Rate Calculation

"""
Tier rate: 
    00.20 000 - 100 kWh
    00.30 101 - 300 kWH
    00.40 301 kwh + 
    10.00 Fixed fee 

Usage Data:
    Day - Time - kWh
"""

def tier_rate_calc(usage_data, t1_rate=00.20, t2_rate=00.30, t3_rate=00.40, fixed_fee=10.00):

    t1_kwh_used         = 0
    t2_kwh_used         = 0
    t3_kwh_used         = 0
    total_cost          = 0
    total_kwh_used      = 0

    # Rate Validation for tiered plan
    match 0:
        case _ if t1_rate == 0:
            raise ValueError("Tier 1 rate cannot be $0.00")
        case _ if t2_rate == 0:
            raise ValueError("Tier 2 rate cannot be $0.00")
        case _ if t3_rate == 0:
            raise ValueError("Tier 3 rate cannot be $0.00")
        case _ if fixed_fee == 0:
            raise ValueError("Fixed fee cannot be $0.00")
        case _:
            pass


    #calc total kwh used
    for day in usage_data:
        kwh = float(day[2])
    
        #kWh Validation
        if(kwh > 0):
            total_kwh_used += kwh
        #negative values treated as 0 usage - no rebate applied.    
        else:
            kwh = 0

    #Tier Distribution
    kwh_remaining   = total_kwh_used

    t1_kwh_used     = min(kwh_remaining, 100)
    kwh_remaining   -= t1_kwh_used

    t2_kwh_used     = min(kwh_remaining, 200)
    kwh_remaining   -= t2_kwh_used

    t3_kwh_used     = kwh_remaining


    #Cost Calculation
    total_cost = round(((t1_kwh_used * t1_rate) + (t2_kwh_used * t2_rate) + (t3_kwh_used * t3_rate)) + fixed_fee, 2)


    return total_cost