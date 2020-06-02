# Django-sql-injection

## What is SQL Injection?

SQL injection is a vulnerability in which malicious data is injected into the application and sent to a SQL database as part of a SQL query and the database executes the malicious query. 

E.g. Consider a login form with the below SQL statement:

SELECT * FROM users WHERE username = ‘$user’ AND password = ‘$password’”; 

In normal scenarios the SQL query would be:

SELECT * FROM users WHERE username = ‘jerin’ AND password = ‘j3rin’;

But an attacker can enter malicious data as below:

SELECT * FROM users WHERE username = ‘jerin OR ‘1’=’1’ --’ AND password = ‘j3rin’;

In the above case, OR ‘1’=’1’ will always make the query TRUE and – will comment the rest of the query and will be ignored. This may lead to authentication bypass altogether.

## Are Django applications vulnerable to SQL Injection? 

A Django application is by default protected against SQL Injection as it uses Object Relational Mapping (ORM). ORM simply means that a developer does not need to write direct SQL queries, but instead uses the in-built QuerySet APIs. Django then converts the Python query to SQL query and communicates with the database.

Now you may ask ‘But in the end it is still an SQL query. Can’t an attacker inject a malicious input and send it as part of that query?’. Well, technically Yes. But that is where the in-built security of Django comes into play. Django’s official documentation states that SQL queries are constructed using query parameterization. A query’s SQL code is defined separately from the query’s parameters. Since parameters may be user-provided and therefore unsafe, they are escaped by the underlying database driver. These two controls of Query Parameterization and Escaping of parameters ensures that Django applications are protected against SQL injection.

But, as the golden rule of security states - “Nothing is 100% secure.'' This case is no exception. There are three scenarios when the application may be vulnerable to SQL injection.
