import csv
import json

csv_file_path = 'c:\\pj3d\\GetDataImport\\bustyle9734_channel_info.csv'
json_file_path = 'c:\\pj3d\\GetDataImport\\bustyle9734_channel_info.json'

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = [row for row in csv_reader]

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)