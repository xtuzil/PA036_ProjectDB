import psycopg2
from psycopg2 import Error
from time import sleep, time
from postgres import PostgresDB
from mongo import MongoDB

postgres = PostgresDB()
time_person_p, time_speed_violation_p = postgres.load_data()
print("Postgres: Loading time for person table is: ", time_person_p)
print("Postgres: Loading time for speed_violation table is: ", time_speed_violation_p)
del postgres


mongo = MongoDB()
time_person_m, time_speed_violation_m = mongo.load_data()
print("MongoDB: Loading time for person table is: ", time_person_m)
print("MongoDB: Loading time for speed_violation table is: ", time_speed_violation_m)

