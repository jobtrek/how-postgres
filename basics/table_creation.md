# Table creation

Tables are one of the central objects you manipulate in a database, a table and his
columns allow you to define the structure of the data you will store on the db.

Once your table is created, the database engine will be able to query it via
SQL commands.

> *[postgres doc - table creation](https://www.postgresql.org/docs/15/tutorial-table.html)*

## Table creation syntax

````sql
CREATE TABLE my_table_name -- specify the table name
(
    -- first the column name, then the type of the column
    my_first_field  text,
    my_second_field int,
    a_date_field    date
);
````

### Table destruction

````sql
DROP TABLE my_table_name;
````

### Concrete example

Creation of a table to store users :

````sql
CREATE TABLE "user"
(
    id        serial PRIMARY KEY,
    name      varchar(60) UNIQUE,
    birthdate date,
    email     varchar(320) UNIQUE
);
````

> Note that “user” table name must be quoted, it’s a reserved keyword.

We will explain types, constraints, key on next chapters.
