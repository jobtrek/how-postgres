# Constraints and indexes

## Basic constraints

In our database, we can use many mechanisms to guard the data that can
be added in a table. For example, the column type will restrict the type of the
data that the column can hold.
In some cases, we need more sophisticated restrictions. Imagine you have a list of
devices, and you want to ensure that the name is not null, and the weight
greater than 0.

Let's create this table :
````sql
CREATE TABLE devices (
    name varchar(100) NOT NULL, -- will ensure no null
    weight int CHECK ( weight > 0 ) -- will ensure that weight is greater than 0
);
````

Now, we want to identify all products with a unique key. The `serial` type
can be used to specify an auto-generated `int` column.
````sql
ALTER TABLE IF EXISTS devices ADD key serial UNIQUE;
````

In this case, the database will automatically create an index. The index will
then be used to check the uniqueness constraint.
Indexes allow far more than that, check the next chapters to discover more :

## Details about constraints and indexes

- [Indexes](./indexes.md)
- [Constraints](./constraints.md)
