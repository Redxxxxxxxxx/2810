#Time Of Use Rate Caculation

"""
Time-of-use rate: 
    00.15 00:00 - 07:00 OFF PEAK
    00.25 07:00 - 18:00 SHOULDER
    00.40 18:00 - 22:00 PEAK
    00.25 22:00 - 00:00 SHOULDER  
    10.00 Fixed fee 

Usage Data: 
    Day - Time - kWh
"""

def time_rate_calc(usage_data, peak_rate=00.40, off_peak_rate=00.15, shoulder_rate=00.25, fixed_fee=10.00):
    
    peak_kwh        = 0
    off_peak_kwh    = 0
    shoulder_kwh    = 0
    kwh_used_cost   = 0
    total_cost      = 0

    #Rate Validation
    match 0:
        case _ if peak_rate == 0:
            raise ValueError("Peak rate cannot be $0.00")
        case _ if off_peak_rate == 0:
            raise ValueError("Off-peak rate cannot be $0.00")
        case _ if shoulder_rate == 0:
            raise ValueError("Shoulder rate cannot be $0.00")
        case _ if fixed_fee == 0:
            raise ValueError("Fixed fee cannot be $0.00")
        case _:
            pass

    #Hour Data Convert to int. Example Output: 17:00:00 --> 1700
    for day in usage_data:

        hour        = int(day[1][0:5].replace(":", ""))
        kwh         = float(day[2])

        #kWh Validation
        if(kwh > 0):
            kwh = kwh
        #negative values treated as 0 usage - no rebate applied.    
        else:
            kwh = 0


        #Calc kwhs Per Timeframe
        match hour:
            #Off Peak
            case time if 0 <= time < 700:
                off_peak_kwh += kwh
            #Shoulder
            case time if 700 <= time < 1800:
                shoulder_kwh += kwh
            #Peak
            case time if 1800 <= time < 2200:
                peak_kwh += kwh
            #Shoulder
            case time if 2200 <= time <= 2359:
                shoulder_kwh += kwh
            #Error
            case _:
                raise ValueError("Invalid Time Period")
    

    #Cost Calculation
    kwh_used_cost += peak_kwh * peak_rate
    kwh_used_cost += off_peak_kwh * off_peak_rate
    kwh_used_cost += shoulder_kwh * shoulder_rate

    total_cost = round((kwh_used_cost + fixed_fee), 2)

    return total_cost