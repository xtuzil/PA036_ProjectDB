from pymongo import MongoClient
from time import time
import json
from Data.DataGenerator import DataGenerator

"""
get_result = {
    "count": lambda x: int(x),
    "find": lambda x: list(x),
    "aggregate": lambda x: list(x),
    "distinct": lambda x: list(x)
}"""


def get_result(method):
    if method == "count":
        return lambda x: int(x)
    if method in ["find", "aggregate", "distinct"]:
        return lambda x: list(x)
    else:
        return lambda x: x


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

        if "mongo" not in yaml_query:
            return 0

        collection = yaml_query["mongo"]["collection"]
        method = yaml_query["mongo"]["method"]
        
        for entry in "filter", "value", "distinct", "projection":
            mongo_query = yaml_query["mongo"]
            if entry in mongo_query:
                args.append({"distinct": lambda x: mongo_query[x]}
                    .get(entry, lambda x: json.loads(mongo_query[x]))(entry))

        if yaml_query["mongo"]["method"] == "update_many":
            print('update many')
            start = time()
            self.person_col.update_many((json.loads(yaml_query["mongo"]["filter"])), (json.loads(yaml_query["mongo"]["value"])), array_filters=(json.loads(yaml_query["mongo"]["arrayFilters"])))
            end = time()
        else:
            # takes collection, method and possibly filters or value and execute it
            start = time()
            result = get_result(method)(getattr(self.get_col(collection), method)(*args))
            end = time()

        # print("Mongo result:", result)

        return end - start
