import psycopg2
from psycopg2 import Error
from time import sleep, time
from postgres import PostgresDB

postgres = PostgresDB()
time_person, time_speed_violation = postgres.load_data()
print("Loading time for person table is: ", time_person)
print("Loading time for speed_violation table is: ", time_speed_violation)
del postgres


