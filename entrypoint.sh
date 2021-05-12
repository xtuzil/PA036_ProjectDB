#!/bin/bash

set -e

su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start"
mongod --fork --dbpath /var/lib/mongo/data --logpath="/dev/null"

python3 main.py
python3 visualization.py
