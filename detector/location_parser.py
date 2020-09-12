import csv

def parse_location(file):
    map = {}
    with open(file) as csvf: 
            csvReader = csv.DictReader(csvf) 
            for rows in csvReader: 
                key = rows['filename'] 
                map[key] = rows 
    return map
