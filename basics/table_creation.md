# Table creation

Tables are one of the central objects you manipulate in a database, a table and his
columns allow you to define the structure of the data you will store on the db.

Once your table is created, the database engine will be able to query it via
SQL commands.

## Table creation syntax

````postgresql
CREATE TABLE my_table_name -- specify the table name
(
    -- first the column name, then the type of the column
    my_first_field  text,
    my_second_field int,
    a_date_field    date
)
````

### Table destruction

````postgresql
DROP TABLE my_table_name;
````

### Concrete example

Creation of a table to store users :
````postgresql
CREATE TABLE "user"
(
    id serial PRIMARY KEY,
    name varchar(60) UNIQUE,
    birthdate date,
    email varchar(320) UNIQUE
);
````
> Note that “user” table name must be quoted, it’s a reserved keyword.

We will explain types, constraints, key on next chapters.
