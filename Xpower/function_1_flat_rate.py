#Flat Rate Calculation

"""
Flat rate: 
    00.25 Per kWh
    10.00 Fixed fee 

Usage Data: 
    Day - Time - kWh
"""

def flat_rate_calc(usage_data, flat_rate=00.25, fixed_fee=10.00):
    
    kwh_used        = 0
    kwh_used_cost   = 0
    total_cost      = 0

    #Rate Validation
    match 0:
        case _ if flat_rate == 0:
            raise ValueError("Flat rate cannot be $0.00")
        case _ if fixed_fee == 0:
            raise ValueError("Fixed fee cannot be $0.00")
        case _:
            pass
    
    #calc total kwh used
    for day in usage_data:
        kwh = float(day[2])
    
        #kWh Validation
        if(kwh > 0):
            kwh_used += kwh
        #negative values treated as 0 usage - no rebate applied.    
        else:
            pass

    #Calc usage cost
    kwh_used_cost = kwh_used * flat_rate

    #Apply fixed fee
    total_cost = kwh_used_cost + fixed_fee
    
    return round(total_cost, 2)