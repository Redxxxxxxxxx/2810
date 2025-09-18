#Test Script

from Xpower.compare_rates   import compare_rates
from process_data               import extract_data

"""
Rate Pricing:
Flat rate: 
    00.25 Per kWh
    10.00 Fixed fee 

Time-of-use rate: 
    00.15 00:00 - 07:00
    00.25 07:00 - 18:00
    00.40 18:00 - 22:00
    00.25 22:00 - 00:00  
    10.00 Fixed fee 

Tier rate: 
    00.20 000 - 100 kWh
    00.30 101 - 300 kWH
    00.40 301 + kWh
    10.00 Fixed fee 

Usage Data: Day - Time - kWh
"""

def main():
    usage_data = extract_data("Xpower/sample_usage_data_month.csv")
    compare_rates(usage_data)

main()