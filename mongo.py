from pymongo import MongoClient
from time import time
import json
from helper import Helper


class MongoDB:
    def __init__(self):
        self._client = MongoClient("mongodb://127.0.0.1:27017")
        self.mongo_db = self._client["pa036"]
        self.mongo_db.person_col.drop()
        self.mongo_db.speed_violation_col.drop()
        self.person_col = self.mongo_db["person"]
        self.speed_violation_col = self.mongo_db["speed_violation"]

    def load_data(self):
        if not Helper.generate():
            return None, None

        # parsing person
        with open('Data/personData.json') as person_data:
            person_list = json.load(person_data)

        start_person = time()
        self.person_col.insert_many(person_list)
        end_person = time()

        # parsing speed_violation
        with open('Data/speedViolationData.json') as speed_violation_data:
            speed_violation_list = json.load(speed_violation_data)

        start_speed_violation = time()
        self.speed_violation_col.insert_many(speed_violation_list)
        end_speed_violation = time()

        return end_person - start_person, end_speed_violation - start_speed_violation

