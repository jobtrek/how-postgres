# How to postgres

> PostgreSQL features summary and tips.

Feel free to contribute with issues and PRs.
This guide is directly inspired by, and regularly refers to,
the official documentation.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/), chose the right distribution installation instructions, don't forget to make the postinstallation steps.

## Setup

```shell
# Clone the repository
git clone git@github.com:jobtrek/how-postgres.git
cd how-postgres
# Start database with docker
docker compose up -d

# After your session, dont forget to stop the containers
docker compose down
```

This docker compose provides a PostgreSQL 18 database with a `postgres`, `password` password and a `training_db` database. The database is accessible on the default port `5432`.

There is also a container with the [pgAdmin](https://www.pgadmin.org/) tool available on [localhost:8080](http://localhost:8080). PgAdmin is a web interface to manage PostgreSQL databases.

## Interacting with the database

There is multiple ways to interact with a PostgreSQL database :

1. From the command line with `psql` tool from inside the docker container : `docker compose exec -it db psql -U postgres -d training_db` This give you acces to a psql shell where you can execute SQL commands.
2. From the command line with `psql` tool from your host machine :
  - Install `psql` on your host machine (search for instructions specific to your OS). E.g. on Debian : `sudo apt install postgresql-client`
  - Connect to the database in the container from your host machine : `psql -h localhost -U postgres -d training_db`
3. From your host machine with a PostgreSQL client like :
  - [DataGrip](https://www.jetbrains.com/datagrip/) : a database IDE from JetBrains.
  - [VSCode postgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) : a PostgreSQL extension for VSCode.
  - [DBeaver](https://dbeaver.io/) : a desktop database management tool.
4. From the pgAdmin web interface available on [localhost:8080](http://localhost:8080).
  - Add a new server with the following parameters :
    - General tab :
      - Name : `Postgres Training`
    - Connection tab :
      - Host name/address : `postgres_db`
      - Port : `5432`
      - Maintenance database : `training_db`
      - Username : `postgres`
      - Password : `password`
    - Click on Save.
  - You should now see the `Postgres Training` server in the left sidebar, you can now expand the menus to explore the database.

## Resources

- [PostgreSQL official documentation](https://www.postgresql.org/docs/current/index.html)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [PostgreSQL Exercises](https://pgexercises.com/)
- [PostgreSQL Cheat Sheet](https://www.tigerdata.com/learn/postgres-cheat-sheet)
- [`psql` documentation](https://www.postgresql.org/docs/current/app-psql.html#usage:~:text=ON_ERROR_STOP%20was%20set.-,Usage,-Connecting%20to%20a)
- [`psql` basics](https://hasura.io/blog/top-psql-commands-and-flags-you-need-to-know-postgresql)

## Loading sample data for testing

Download the sample data from [here](https://github.com/h8/employees-database) and load it into the database. This is a sample employees database with multiple tables and relations.

```shell
# Download the sample data
wget https://raw.githubusercontent.com/h8/employees-database/refs/heads/master/employees_data.sql.bz2
# Unzip the sample data
bzip2 -d employees_data.sql.bz2
# Load the sample data into the database (with psql from the host machine)
psql -h localhost -U postgres -d training_db -f employees_data.sql
```
