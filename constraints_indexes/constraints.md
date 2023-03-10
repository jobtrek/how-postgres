# Constraints

As we have seen, constraints are frequently using indexes, this is due to the fact
that the database will need index to efficiently check the constraint.
But there is many more to do with constraints.

## Check constraint

Check constraints are really simple, you just specify a boolean expression.
Note that a check constraint can only be based on the query data.

A simple example, where we check products characteristics :

````sql
CREATE TABLE products
(
    id     serial PRIMARY KEY,
    weight numeric(2) CHECK ( weight > 10 ), -- simple comparison operators
    size   numeric(2) CHECK ( size <= 10 )
);
````

We can do more multiple checks :

````sql
ALTER TABLE products
    ADD COLUMN price numeric(2) CHECK ( price > 1 AND price < 100 );
````

Constraints can be named :

````sql
ALTER TABLE products
    ADD COLUMN discount numeric(2)
        CONSTRAINT minimum_discount CHECK ( discount > 2 );
````

You can also call functions in constraints. **Warning :** be careful, because if
the function is modified, the integrity of the constraint will no longer be guaranteed.

```sql
ALTER TABLE products
    ADD COLUMN name varchar(200) CHECK ( CHAR_LENGTH(name) > 10 ); -- check the length of the string
```

## Uniqueness constraints

You can use the unique keyword, the database will then ensure that there are no
duplicates in the column.

````sql
CREATE TABLE books
(
    id            serial PRIMARY KEY,
    serial_number varchar(20) UNIQUE -- Uniqueness constraint
);
````

Unique constraint can be also be a combination of fields. Each fields individually
will not be forced to be unique, but the combination of two have to be unique.

````sql
CREATE TABLE permissions
(
    entity  varchar(30) NOT NULL, -- not null is also a constraint
    ability varchar(10) NOT NULL,
    UNIQUE (entity, ability)
);
````

## Primary keys and foreign keys

To maintain integrity between tables, the database engine will use keys, these
keys are unique identifiers for a table row. It is mandatory that the keys are
unique, so that the database can identify the data.

We can use special keywords to declare keys.
Primary keys :

````sql
CREATE TABLE events
(
    id   serial PRIMARY KEY,
    name varchar(100) NOT NULL
);
````

There is also a keyword to declare foreign keys :
```sql
CREATE TABLE speakers
(
    id serial PRIMARY KEY,
    name varchar(100) NOT NULL,
    event_id integer REFERENCES events -- event_id is the foreign key to events id
);
```

> More details about the `REFERENCES` keyword in the *Foreign keys* chapter.

> *[postgres docs - constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)*
