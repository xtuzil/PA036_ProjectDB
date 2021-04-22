FROM fedora:34

RUN dnf -y update --nogpgcheck

# Postgres
RUN dnf -y install postgresql postgresql-server python3-psycopg2

# Mongo 
RUN echo $'[mongodb-upstream]\n\
name=MongoDB Upstream Repository\n\
baseurl=https://repo.mongodb.org/yum/redhat/8Server/mongodb-org/4.2/x86_64/\n\
gpgcheck=1\n\
enabled=1\n\
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc' \
> /etc/yum.repos.d/mongodb.repo

RUN dnf -y --nogpgcheck install mongodb-org python3-pymongo

RUN dnf -y --nogpgcheck install procps git
RUN dnf -y --nogpgcheck install python3-pip

RUN pip3 install pyaml

RUN \
su - postgres -c "/usr/bin/initdb" && \
su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start" && \
su - postgres -c "createdb pa036" && \
su - postgres -c "createuser admin" && \
su - postgres -c "/usr/bin/pg_ctl stop" && \
:

RUN mkdir -p /var/lib/mongo/data

WORKDIR "/root/pa036"

CMD ["/root/pa036/entrypoint.sh"]

## Run as:
# podman run -it --privileged --mount type=bind,source=".",target="/root/pa036" databases

################################################################################
# This is no longer needed

## To initialize PostgreSQL database
# su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start"

## Postgres shell
# su - postgres -c "psql"

## To initialize MongoDB database
# mongod --dbpath /var/lib/mongo/data 2>&1 > /dev/null &

## Mongo shell
# mongo
