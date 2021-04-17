# PA036_ProjectDB
Repository to PA036 project DB

## Requirements
* Python 3
* PostgreSQL  
* MongoDB
* Psycopg2
* PyMongo
* PyYAML


## Instalation

### Postgres  

MacOS - `brew install postgresql`  
Linux - ???  
Windows - ???

### MongoDB
MacOS - `brew install mongodb-community@4.4`  
Linux - ???  
Windows - ???

### Psycopg2    
$`pip install psycopg2`

### PyMongo 
$`python -m pip install pymongo`

### PyYAML 
$`pip install PyYAML`


## Creating Postgres db
$`initdb /usr/local/var/postgres`  
$`pg_ctl -D /usr/local/var/postgres start`  
$`createdb pa036`  
$`psql pa036`  
$`CREATE USER admin WITH SUPERUSER PASSWORD 'admin';` (to psql)    
$`exit`

## Data preparation
You must provide file personData.json in Data directory. If the file is zipped, unzip it with:  
$`gunzip -k personData.json.gz`


## Running the app
Just run main() in main.py


## DEV notes
To disable loading the data every time:
* comment calling the function `load_data()` for both db
* in MongoDB `__init__()` comment dropping both collection 
* in Postgres `__init__()` comment loop with executing commands 

## TODO
* environment pro $lookup
* wiriting times to csv file
