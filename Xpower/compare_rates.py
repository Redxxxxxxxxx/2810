#Compare All Rate Price Calculations

from Xpower.flat_rate       import flat_rate_calc
from Xpower.time_use_rate   import time_rate_calc
from Xpower.tier_rate       import tier_rate_calc



def compare_rates(usage_data):
    
    rate_calcs              = []
    
    #Call Previous Functions To Run Comparison For User - [[Rate Type, Cost], []...] 
    rate_calcs.append(["Flat Rate", flat_rate_calc(usage_data)])
    rate_calcs.append(["Time Rate", time_rate_calc(usage_data)])
    rate_calcs.append(["Tier Rate", tier_rate_calc(usage_data)])

    #Find Cheapest Offering
    cheap_rate, cheap_cost  = rate_calcs[0]

    for rate_type in rate_calcs[1:]:
            if (rate_type[1] < cheap_cost):
                cheap_cost = rate_type[1]
                cheap_rate = rate_type[0]
            else:
                pass


    #Function Prints Here For Demonstrative Output Of Assignment Rather Than Returning Values To A Main
    #Output All Plan Costs For User:
    for rate in rate_calcs:
        print(f"Your {rate[0]} Plan Cost Will Be: ${rate[1]}")

    #Identiy Cheapest Offering
    print(f"Your Cheapest Plan Will Be {cheap_rate} With A Cost Of: ${cheap_cost}")