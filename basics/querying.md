# Querying our tables

Retrieve all data in a table :

````sql
SELECT * FROM "user";
````

`*` is a wildcard, it indicates that you want all table columns.
You can retrieve specific columns by naming it :
````sql
SELECT name, email FROM "user";
````

Be careful, the upper commands will retrieve all table rows, that could cause
performance problems if your table holds many rows.
You can limit the number of returned rows :
````sql
SELECT * FROM "user" LIMIT 2;
````

You can easily order your query results, for example by name :
````sql
SELECT * FROM "user" ORDER BY name LIMIT 10;
````

Specify query conditions with the `WHERE` clause :

````sql
SELECT * FROM "user" WHERE name = 'Titi'; -- Gets only Titi

SELECT * FROM "user" WHERE birthdate < '2000-01-01'; -- selects dates before 2000
````

> *[postgres doc - querying a table](https://www.postgresql.org/docs/15/tutorial-select.html)*
