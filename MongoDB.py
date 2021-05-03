from pymongo import MongoClient
from time import time
import json
from Data.DataGenerator import DataGenerator

get_result = {
    "count": lambda x: int(x),
    "find": lambda x: list(x),
}

class MongoDB:
    def __init__(self):
        self._client = MongoClient("mongodb://127.0.0.1:27017")
        self.mongo_db = self._client["pa036"]
        self.mongo_db["person"].drop()
        self.mongo_db["speed_violation"].drop()
        self.person_col = self.mongo_db["person"]
        self.speed_violation_col = self.mongo_db["speed_violation"]

    def load_data(self):
        if not DataGenerator.generate():
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

    def get_col(self, col_name: str):
        if col_name == "person":
            return self.person_col
        elif col_name == "speed_violation":
            return self.speed_violation_col
        else:
            return None

    def execute_query(self, yaml_query):
        args = []

        collection = yaml_query["mongo"]["collection"]
        method = yaml_query["mongo"]["method"]
        if "filter" in yaml_query["mongo"]:
            args.append(json.loads(yaml_query["mongo"]["filter"]))
        if "value" in yaml_query["mongo"]:
            args.append(json.loads(yaml_query["mongo"]["value"]))

        # takes collection, method and possibly filters or value and execute it
        start = time()
        result = get_result[method](getattr(self.get_col(collection), method)(*args))
        end = time()
        print("Mongo result:", result)

        return end - start


