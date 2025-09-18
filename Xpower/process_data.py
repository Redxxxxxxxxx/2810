#Process Sample Usage Data

def extract_data(data):
    usage_data = []

    with open(data) as data:
        for line in data:
            val             = line.split()
            date            = val[0][-2:]
            hour, kwh       = val[1].split(",")

            data_set = [date, hour, kwh]

            usage_data.append(data_set)

    return usage_data