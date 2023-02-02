# Indexes

Indexes are one of the most powerful features of a database system.
They allow many features like :
- Accelerating searches through your tables.
- Allowing to efficiently check uniqueness constraints.

There are many other benefits of indexes, but keep in mind one trade-off, indexes
need to be updated on each writes, thus, the write performances could be affected
on large indexes.

The next chapter will travel through the main indexes functionalities with postgres.

## Basics

IImagine you create a database to store users. You have many users, let's say,
1 million. So you have a table users, and in this table you have an id and a name column.
Now, you want to search a user with the id 500'000. Your database will have
to walk through the 500'000 first elements to find the record.
This is a terrible performance bottleneck, imagine, each request to your database
will need to walk tons of records each time.

Indexes are a specific kind of data structure imagined to optimise search time
in a large amount of data. The index will allow the database to travel a table
extremely fast, and therefore accelerate your queries.

> If you want more details about indexes internal mechanism, feel free to follow
> links below.

### Creating an index

You can use `CREATE INDEX` to generate a new index on an existing table.

````sql
CREATE TABLE my_table ( -- table creation
    my_field int
);

CREATE INDEX my_field_index ON my_table (my_field); -- add index on my_field
````
The database will now maintain an index on the `my_field` column, and next requests
can be accelerated by the index.

> WARNING : adding an index doesn't mean performance boost, in some cases this
> may even lead to a loss of performance. It's important to understand the
> specificities of indexes to correctly use them.

## Typical index situations

## Index types


> *[postgres docs - indexes](https://www.postgresql.org/docs/current/indexes.html)*
