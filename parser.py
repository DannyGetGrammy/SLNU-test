import pandas as pd


def parse_line(line):
    parts = line.strip().split()
    return {
        'index': int(parts[0].replace(',', '')),
        'time_from_start': int(parts[1]),
        'date': parts[2],
        'time': parts[3],
        'event_type': int(parts[4]),
        'glucose': int(parts[5]),
        'trend': float(parts[6]),
        'insulin_delivered': float(parts[7]),
        'carbs': int(parts[8]),
        'food_delivered': float(parts[9]),
        'correction_delivered': float(parts[10].replace(';', ''))
    }


parsed_data = data[0].apply(parse_line).tolist()
