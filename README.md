# PA036_ProjectDB
Repository to PA036 project DB


## Instalation
Req: Python 3


### Postgres  

MacOS - brew install postgresql  
Linux - ???  
Windows - ???

#### Psycopg2 module   
pip install psycopg2 


### MongoDB
brew install mongodb-community@4.4

PyMongo
python -m pip install pymongo


### Creating Postgres db
initdb /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres start
createdb pa036
psql pa036
CREATE USER admin WITH SUPERUSER PASSWORD 'admin'; (to psql)
exit