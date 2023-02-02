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



> *[postgres docs - indexes](https://www.postgresql.org/docs/current/indexes.html)*
