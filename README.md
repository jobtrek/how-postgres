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

1. From the command line with `psql` tool :
  ```shell
  docker compose exec -it db psql -U postgres -d training_db
  ```
  This give you acces to a psql shell where you can execute SQL commands. See [psql Usage](https://www.postgresql.org/docs/current/app-psql.html#usage:~:text=ON_ERROR_STOP%20was%20set.-,Usage,-Connecting%20to%20a) for more information.
1. From your host machine with a PostgreSQL client like :
  - [DataGrip](https://www.jetbrains.com/datagrip/) : a database IDE from JetBrains.
  - [VSCode postgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) : a PostgreSQL extension for VSCode.
  - [DBeaver](https://dbeaver.io/) : a desktop database management tool.
1. From the pgAdmin web interface available on [localhost:8080](http://localhost:8080).
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
    
## Summary

- [Architecture](./architecture.md)
- [Installation](./installation.md)
- **Basics :**
  - [Users and databases](./basics/users_database.md)
  - [Accessing database](./basics/accessing_database.md)
  - [Table creation](./basics/table_creation.md)
  - [Inserting data in table](./basics/inserting_data.md)
  - [Querying your tables](./basics/querying.md)
  - [Updating table data](./basics/updating.md)
  - [Delete table data](./basics/deleting.md)
  - [Aggregates](./basics/aggregates.md)
- [Constraints and indexes](./constraints_indexes)
  - [Indexes](./constraints_indexes/indexes.md)
  - [Constraints](./constraints_indexes/constraints.md)

TODOS :
- Constraints and indexes
- Joins
- Advanced queries
- Views
- Usefully data types
- Techniques
  - Window functions
  - Analyse query planning
  - Full text search
  - Materialised views
  - Performance tuning
  - Partitioning
