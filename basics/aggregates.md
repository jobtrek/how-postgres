# Aggregates

Postgres provides some functions that allow you to aggregate data in your
query requests.

You can count rows :

````sql
SELECT COUNT(*)
FROM "user";
````

Or select the maximum value in a specified column :

````sql
SELECT MAX(birthdate)
FROM "user"; -- Will return only the max value
````

You can combine aggregate function with grouping, that will result in a histogram :

````sql
SELECT DATE_TRUNC('year', birthdate) AS year, COUNT(*)
FROM "user" -- date trunc conserves only specified part of the date
GROUP BY year;
````

> *[postgres doc - aggregate functions](https://www.postgresql.org/docs/15/tutorial-agg.html)*
