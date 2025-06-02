import csv
from datetime import datetime

CSV_FILE = 'Tandem_daily_timeline small sample - Sheet1.csv'


def parse_csv(file_path):
    events = []
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        # Skip first 6 lines of metadata
        for _ in range(6):
            next(reader, None)
        dataset = None
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            if row[0] in {'DeviceType', 'Type'}:
                # Determine dataset type based on header row
                if row[0] == 'DeviceType' and 'Readings (mg/dL)' in row:
                    dataset = 'EGV'
                elif row[0] == 'DeviceType' and 'BG (mg/dL)' in row:
                    dataset = 'BG'
                elif row[0] == 'Type':
                    dataset = 'Bolus'
                continue
            if dataset == 'EGV':
                events.append({
                    'timestamp': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'event_type': row[2].strip(),
                    'serial_number': row[1].strip(),
                    'glucose_mgdl': row[4].strip()
                })
            elif dataset == 'BG':
                note = row[5].strip() if len(row) > 5 else ''
                events.append({
                    'timestamp': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'event_type': row[2].strip(),
                    'serial_number': row[1].strip(),
                    'bg_mgdl': row[4].strip(),
                    'note': note
                })
            elif dataset == 'Bolus':
                # Ensure row has enough columns by padding
                row += [''] * (20 - len(row))
                events.append({
                    'timestamp': datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),
                    'event_type': 'Bolus',
                    'bolus_type': row[1].strip(),
                    'delivery_method': row[2].strip(),
                    'bg_mgdl': row[3].strip(),
                    'serial_number': row[4].strip(),
                    'insulin_delivered': row[6].strip(),
                    'food_delivered': row[7].strip(),
                    'correction_delivered': row[8].strip(),
                    'completion_status': row[9].strip(),
                    'bolex_start': row[10].strip(),
                    'bolex_completion': row[11].strip(),
                    'bolex_insulin': row[12].strip(),
                    'bolex_status': row[13].strip(),
                    'standard_percent': row[14].strip(),
                    'duration_mins': row[15].strip(),
                    'carb_size': row[16].strip(),
                    'target_bg': row[17].strip(),
                    'correction_factor': row[18].strip(),
                    'carb_ratio': row[19].strip()
                })
    return events


def main():
    events = parse_csv(CSV_FILE)
    events.sort(key=lambda e: e['timestamp'])
    for e in events:
        print(e)


if __name__ == '__main__':
    main()
