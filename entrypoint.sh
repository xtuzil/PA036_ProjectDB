#!/bin/bash

su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start"
mongod --dbpath /var/lib/mongo/data 2>&1 > /dev/null &

python3 main.py

# Continue with shell
exec bash
