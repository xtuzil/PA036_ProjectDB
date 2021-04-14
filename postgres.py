from psycopg2 import connect, Error
from time import time
import json
from Data.GenerateSpeedViolationData import SpeedViolationDataGenerator

SPEED_VIOLATION_RECORDS_COUNT = 100000

commands = (
        """
        DROP TABLE IF EXISTS person, speed_violation;
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
            for command in commands:
                self.cursor.execute(command)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # load person json data to the table as jsonb --- as json, it is twice more quicker
    def load_data(self):

        # Generate data
        try:
            f = open("Data/personData.json")
            # Do something with the file
        except IOError:
            print("File not accessible")
            return
        finally:
            f.close()

        SpeedViolationDataGenerator.generate_speed_violation("Data/personData.json", SPEED_VIOLATION_RECORDS_COUNT)

        # parsing person
        with open('Data/personData.json') as person_data:
            person_list = json.load(person_data)

        sql_string_person = 'INSERT INTO person (data) VALUES '

        for record in person_list:
            person = json.dumps(record)
            sql_string_person += "('" + person + "'::jsonb),"

        # remove the last comma and end statement with a semicolon
        sql_string_person = sql_string_person[:-1] + ";"

        # parsing speed_violation
        with open('Data/speedViolationData.json') as speed_violation_data:
            speed_violation_list = json.load(speed_violation_data)

        sql_string_speed_violation = 'INSERT INTO speed_violation (data) VALUES '

        for record in speed_violation_list:
            speed_violation = json.dumps(record)
            sql_string_speed_violation += "('" + speed_violation + "'::jsonb),"

        # remove the last comma and end statement with a semicolon
        sql_string_speed_violation = sql_string_speed_violation[:-1] + ";"

        print(speed_violation)

        try:
            start_person = time()
            self.cursor.execute(sql_string_person)
            end_person = time()

            start_speed_violation = time()
            self.cursor.execute(sql_string_speed_violation)
            end_speed_violation = time()

            self.connection.commit()

            print('\nfinished INSERT INTO execution')
            return end_person - start_person, end_speed_violation - start_speed_violation

        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            self.connection.rollback()

    def example(self):
        # Executing a SQL query

        self.cursor.execute("SELECT * FROM person;")

        # Fetch result
        record = self.cursor.fetchone()
        print("Persons: ", record, "\n")

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

