import csv
import json

rows = ['Date_Time', 'Shape', 'Duration', 'City', 'State', 'Lat', 'Lng']
with open('sightings_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows += [row]

print(json.dumps(rows, sort_keys=True, indent=4, separators=(',', ': ')))