# Inserting data in a table

You can insert data in a table with :

```sql
INSERT INTO "user" (name, birthdate, email) -- Specify the columns you want to insert in
VALUES ('Toto', '1998-10-15', 'toto@test.dev'); -- Specify your data
```

You can insert multiple sets of values in one command :

````sql
INSERT INTO "user" (name, birthdate, email)
VALUES ('Tutu', '2000-02-20', 'tutu@test.dev'),
       ('Titi', '2002-04-06', 'titi@test.dev'); -- Multiple rows of data
````

> *[postgres doc - inserting](https://www.postgresql.org/docs/15/tutorial-populate.html)*
