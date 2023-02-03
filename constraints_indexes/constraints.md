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
    weight decimal CHECK ( weight > 10 ), -- simple comparison operators
    size   decimal CHECK ( size <= 10 )
);
````

> *[postgres docs - constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)*
