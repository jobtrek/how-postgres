# Basics - users and databases

When you start working on a project that needs to access the database, best
practices would tell you to create a new user, database and schema.
These steps allows you to securely split your different accesses to databases (via
roles and access rights) and organise efficiently your work.

The next few lines go through the different commands to manage users, db, and
schemas.

If you need more advanced user or schema management techniques, feel free to
investigate relevant chapters of the official documentation.

## Vocabulary

- **user** : Exactly what you think, you can create users and give them accesses
  to certain databses. Like users files rights on your OS.
- **database** : Here will be stored all the things related to your project database,
  typically tables, indexes, views. You will typically have one database per "project".
- **schema** : You can see it like namespaces, that allows you to separate tables
  in "subcategories" -> the schema.

## Accessing your database server

Depending on your installation, the connection will vary. On Unix-like systems,
you access postgreSQL command interface via :

```shell
sudo -u postgres psql
```

This will launch the psql command with the postgres user.

## Creating user and database

When you are connected to the database server (with a user with sufficient rights,
like the *postgres* global database administrator) you can try your first user
creation commands.

### Create a fresh user :

```postgresql
CREATE USER yourusername WITH ENCRYPTED PASSWORD 'yourpass';
```
> You can create users with other
> [authentication techniques than password](https://www.postgresql.org/docs/current/client-authentication.html),
> we will stay with password in this tutorial.

### Create a new database

````postgresql
CREATE DATABASE yourdatabasename;
````

### Get your user access to the newly created database

````postgresql
GRANT ALL PRIVILEGES ON DATABASE yourdatabasename TO yourusername;
````

> You can specify more advanced user privileges, see official docs.
