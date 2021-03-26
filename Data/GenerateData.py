import json
import random
import time
from datetime import timedelta

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y', prop)

def random_date_custom():
    return random_date("1/1/2008", "1/3/2021", random.random())


# retrieve license plates json data 
def retrieve_license_plates(file):
    with open(file, "r") as read_file:
        data = json.load(read_file)

    license_plates = []

    for person in data:
        for car in person['cars']:
            license_plates.append(car['license_plate'])

    return license_plates


#create json data for speed_violation 
def generate_speed_violation(input_file, n):

    license_plates = retrieve_license_plates(input_file)

    limits = [30, 40, 50, 70, 90, 100, 130]
    res_document = []
    for i in range(n):
        license_plate = random.choice(license_plates)
        random_d = random_date_custom()
        limit = random.choice(limits)
        actual_speed = random.randint(limit+5, 200)

        res_document.append({
        'license_plate': license_plate,
        'date': random_d,
        'speed_limit': limit,
        'actual_speed': actual_speed
        })


    with open('speed_violation.json', 'w') as outfile:
        json.dump(res_document, outfile)


generate_speed_violation("data.json", 100)





