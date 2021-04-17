import psycopg2
from psycopg2 import Error
from time import sleep, time
import yaml
import csv
from Postgres import PostgresDB
from MongoDB import MongoDB


class ExperimentApp:

    def __init__(self):
        self.postgres = PostgresDB()
        self.mongo = MongoDB()

    def run(self):

        time_person_p, time_speed_violation_p = self.postgres.load_data()
        print("Postgres: Loading time for person table is: ", time_person_p)
        print("Postgres: Loading time for speed_violation table is: ", time_speed_violation_p)

        time_person_m, time_speed_violation_m = self.mongo.load_data()
        print("MongoDB: Loading time for person table is: ", time_person_m)
        print("MongoDB: Loading time for speed_violation table is: ", time_speed_violation_m)

        with open("queries.yaml", 'r') as stream:
            queries = yaml.safe_load(stream)

        for query in queries["queries"]:
            query_id = query["id"]
            desc = query["description"]
            print(f"\nRunning query #{query_id}:", desc)

            mongo_time = self.mongo.execute_query(query)
            postgres_time = self.postgres.execute_query(query)

            print("Mongo time:", mongo_time)
            print("Postgres time:", postgres_time)

            # second time because cache?
            """mongo_time = self.mongo.execute_query(query)
            postgres_time = self.postgres.execute_query(query)

            print("Mongo time with cache applied:", mongo_time)
            print("Postgres time with cache applied:", postgres_time)"""




