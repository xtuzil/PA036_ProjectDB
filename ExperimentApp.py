import psycopg2
from psycopg2 import Error
from time import sleep, time
import yaml
import csv
from Postgres import PostgresDB
from MongoDB import MongoDB
import json
import os

class ExperimentApp:

    def __init__(self):
        self.postgres = PostgresDB()
        self.mongo = MongoDB()

    def run(self):
        
        psql_index_text = {
            "": "PostgreSQL binary json",
            "jsonb_ops": "PostgreSQL with index ",
            "jsonb_path_ops": "PostgreSQL with index",
        }
        
        # Change this to one of the valid keys in `psql_index_text`
        psql_index = ""
        
        results_json = {}
        
        if os.path.isfile("results.json"):
            with open("results.json", "r") as result_file:
                results_json = json.load(result_file)
        
        with open("queries.yaml", 'r') as stream:
            queries = yaml.safe_load(stream)
        
        def default_result(name, inner_name, *args):
            # optional description argument
            desc = name if len(args) == 0 else args[0]
            
            return results_json.setdefault(name, {
                "description": desc,
                "columns": {},
            })["columns"].setdefault(inner_name, [])
        
        def run_mongo():
            time_person_m, time_speed_violation_m = self.mongo.load_data()
            print("MongoDB: Loading time for person table is: ", time_person_m)
            print("MongoDB: Loading time for speed_violation table is: ", time_speed_violation_m)
            
            default_result("Data loading person", "MongoDB").append(time_person_m)
            default_result("Data loading speed_violation", "MongoDB").append(time_speed_violation_m)
            
            for query in queries["queries"]:
                query_id = query["id"]
                desc = query["description"]
                print(f"\nRunning query #{query_id}:", desc)

                mongo_time = self.mongo.execute_query(query)

                print("Mongo time:", mongo_time)
                
                default_result(str(query_id), "MongoDB", desc).append(mongo_time)
        
        def run_postgres():
            time_person_p, time_speed_violation_p, time_person2_p = self.postgres.load_data(psql_index)
            print("Postgres: Loading time for person table (INSERT with all data) is: ", time_person_p)
            print("Postgres: Loading time for speed_violation table (INSERT with all data) is: ", time_speed_violation_p)
            print("Postgres: Loading time for person2 table (convert and using copy function, no id) is: ", time_person2_p)
            
            default_result("Data loading person", psql_index_text[psql_index] + psql_index).append(time_person_p)
            default_result("Data loading speed_violation", psql_index_text[psql_index] + psql_index).append(time_speed_violation_p)
            
            for query in queries["queries"]:
                query_id = query["id"]
                desc = query["description"]
                print(f"\nRunning query #{query_id}:", desc)

                postgres_time = self.postgres.execute_query(query)

                print("Postgres time:", postgres_time)
                
                # The text here needs to match one of the values in visualization.py
                # dicitonary `columns`
                default_result(str(query_id), "MongoDB", desc).append(postgres_time)
        
        run_mongo()
        run_postgres()
            
        with open("results.json", "w") as result_file:
            json.dump(results_json, result_file, indent = 2)
