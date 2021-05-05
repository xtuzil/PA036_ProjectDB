from psycopg2 import connect, Error
from time import time
import json
from Data.DataGenerator import DataGenerator
import os
import jsonlines

commands = (
        """
        DROP TABLE IF EXISTS person, speed_violation, person2;
        """,
        """
        CREATE TABLE person (
            id serial NOT NULL PRIMARY KEY,
            data jsonb
        )
        """,
        """ 
        CREATE TABLE speed_violation (
            id serial NOT NULL PRIMARY KEY,
            data jsonb
        )
        """,
        """
        CREATE TABLE person2 (
            data jsonb
        )
        """
)


class PostgresDB:
    def __init__(self):
        try:
            self.connection = connect("dbname=pa036 user=admin host=localhost password=admin")
            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()

            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(self.connection.get_dsn_parameters(), "\n")

            # Create tables
            #for command in commands:
                #self.cursor.execute(command)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # load person json data and speed_violation json data to the table as jsonb
    def load_data(self):

        if not DataGenerator.generate():
            return None, None

        # parsing person
        with open('Data/personData.json') as person_data:
            person_list = json.load(person_data)

        sql_string_person = 'INSERT INTO person (data) VALUES '

        for record in person_list:
            person = json.dumps(record)
            sql_string_person += f"('{person}'::jsonb),"

        # remove the last comma and end statement with a semicolon
        sql_string_person = sql_string_person[:-1] + ";"

        # parsing speed_violation
        with open('Data/speedViolationData.json') as speed_violation_data:
            speed_violation_list = json.load(speed_violation_data)

        sql_string_speed_violation = 'INSERT INTO speed_violation (data) VALUES '

        for record in speed_violation_list:
            speed_violation = json.dumps(record)
            sql_string_speed_violation += f"('{speed_violation}'::jsonb),"

        # remove the last comma and end statement with a semicolon
        sql_string_speed_violation = sql_string_speed_violation[:-1] + ";"

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        sql_string_person2 = 'copy person2 from \'%s/Data/person.json\';' % ROOT_DIR

        try:
            start_person = time()
            self.cursor.execute(sql_string_person)
            end_person = time()

            start_speed_violation = time()
            self.cursor.execute(sql_string_speed_violation)
            end_speed_violation = time()

            start_person2 = time()
            with open('%s/Data/personData.json' % ROOT_DIR, 'r') as f:
                json_data_normal = json.load(f)
            with jsonlines.open('%s/Data/person.json' % ROOT_DIR, 'w') as writer:
                writer.write_all(json_data_normal)
            self.cursor.execute(sql_string_person2)
            end_person2 = time()

            self.connection.commit()

            return end_person - start_person, end_speed_violation - start_speed_violation, end_person2 - start_person2

        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            self.connection.rollback()

    def execute_query(self, yaml_queries):

        if "postgres" not in yaml_queries:
            return 0

        start = time()
        self.cursor.execute(yaml_queries["postgres"])
        record = self.cursor.fetchone()
        print("Postgres result: ", record)
        end = time()
        return end - start

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

