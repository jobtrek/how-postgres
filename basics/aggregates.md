# Aggregates

Postgres provides some functions that allow you to aggregate data in your
query requests.

You can count rows :
````sql
SELECT count(*) FROM "user";
````

Or select the maximum value in a specified column :
````sql
SELECT max(birthdate) FROM "user"; -- Will return only the max value
````

You can combine aggregate function with grouping, that will result in a histogram :
````sql
SELECT date_trunc('year', birthdate) AS year, count(*) FROM "user" -- date trunc conserves only specified part of the date
    GROUP BY year;
````

> *[postgres doc - aggregate functions](https://www.postgresql.org/docs/15/tutorial-agg.html)*
