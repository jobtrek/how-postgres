# Updating table data

You can update a row in your tables, never forget the where clause to identifies
the row to update.

````sql
UPDATE "user"
SET birthdate = '2010-10-10'
WHERE id = 1;
````

You can update multiple rows, for example shift dates :

````sql
UPDATE "user"
SET birthdate = birthdate + INTERVAL '6 months' -- add 6 month to dates
WHERE birthdate > '2002-01-01'; -- only update birthdate after january 2002
````

> *[postgres doc - updating](https://www.postgresql.org/docs/15/tutorial-update.html)*
