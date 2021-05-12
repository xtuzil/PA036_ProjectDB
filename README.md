# PA036_ProjectDB
Repository to PA036 project DB  

#### Team mebers: 
Katarina Hermanova, 
Marian Koncek, 
Matej Tuzil, 
Vojtech Spevak


In Fedora 33 please run this project in /tmp/ file to avoid "Permission denied" type of errors (sorry for inconveniences)
In Windows run this project from Public folder or set the permissions as described in Data preparation section

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

Fedora 33 + DB setup (can skip Creating Postgres db below):                     
$`sudo dnf update -y`                                        
$`sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-33-x86_64/pgdg-fedora-repo-latest.noarch.rpm`             
$`sudo dnf install -y postgresql13-server`                                                 
$`sudo /usr/pgsql-13/bin/postgresql-13-setup initdb`                                              
$`sudo systemctl enable postgresql-13`                                  
$`sudo systemctl start postgresql-13`                                    
$`sudo systemctl status postgresql-13`                              
$`sudo su - postgres`                            
$`psql`                                          
$`alter user postgres with password 'admin@123';`               
$`CREATE USER admin WITH SUPERUSER PASSWORD 'admin';`                    
$`create database pa036;`                                    
$`exit`                                    
$`logout`

Windows - Download the installer from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads and follow the installation.

### MongoDB
MacOS - `brew install mongodb-community@4.4`  

Fedora 33:                                   
$`sudo dnf install nano`                               
$`sudo nano /etc/yum.repos.d/mongodb.repo`              
add and save:    
```
[mongodb-org-4.4]      
name=MongoDB Repository   
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/4.4/x86_64/     
gpgcheck=1      
enabled=1      
gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc
```
$`sudo dnf install mongodb-org`       
$`sudo systemctl daemon-reload`      
$`sudo systemctl start mongod`      
$`sudo systemctl status mongod`        
$`mongod -version`     
 
Windows - Follow the steps desribed in https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/ including setting up the mongodb as a windows service.

### Psycopg2    
$`pip install psycopg2`   

Fedora 33:   
$`sudo yum install libpq-devel python-devel`          
$`pip install psycopg2` (if run with error continue below)     
$`pip install psycopg2-binary`       
$`pip freeze | grep psycopg2`      

### PyMongo 
$`python -m pip install pymongo`

### PyYAML 
$`pip install PyYAML`

### jsonlines
$`pip install jsonlines`

### matplotlib
in Fedora 33: $`sudo dnf install python3-matplotlib.x86_64`      
$`pip install matplotlib`

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

Windows - set the access permissions of person.json: `Properties -> Security -> Edit -> Add -> "yourcomputername\Users"`

## Running the app
Just run main() in main.py

