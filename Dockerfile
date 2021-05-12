## Before build:
# docker pull fedora:34

## Build:
# docker build . -t databases

## Run as:
# docker run --rm --privileged --mount type=bind,src=.,dst=/opt/pa036 -it databases

################################################################################

FROM fedora:34

# Mongo repository
RUN echo $'[mongodb-upstream]\n\
name=MongoDB Upstream Repository\n\
baseurl=https://repo.mongodb.org/yum/redhat/8Server/mongodb-org/4.2/x86_64/\n\
gpgcheck=1\n\
enabled=1\n\
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc' \
> /etc/yum.repos.d/mongodb.repo

RUN dnf -y install postgresql postgresql-server python3-psycopg2 mongodb-org python3-pymongo python3-pip python3-matplotlib nano

RUN pip3 install pyaml jsonlines

# Initialize PostgreSQL database with initial tables and users
RUN \
su - postgres -c "/usr/bin/initdb" && \
su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start" && \
su - postgres -c "createdb pa036" && \
su - postgres -c "createuser --superuser admin" && \
su - postgres -c "/usr/bin/pg_ctl stop" && \
:

# Intialize a place for MongoDB to store data
RUN mkdir -p /var/lib/mongo/data

WORKDIR "/opt/pa036"

CMD ["/opt/pa036/entrypoint.sh"]
