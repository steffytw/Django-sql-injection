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
First, Django’s implementation of Query Parameterization and Escaping of parameters in some cases may not be perfect. After all it is done by humans, and humans make errors. A search for Django in https://cve.mitre.org will show a vulnerability numbered CVE-2014-0474. The vulnerability is described as “The (1) FilePathField, (2) GenericIPAddressField, and (3) IPAddressField model field classes in Django before 1.4.11, 1.5.x before 1.5.6, 1.6.x before 1.6.3, and 1.7.x before 1.7 beta 2 do not properly perform type conversion, which allows remote attackers to have an unspecified impact and vectors, related to "MySQL type casting." This simply means that the controls to prevent SQL injection was not properly implemented in FilePathField, GenericIPAddressField and IPAddressField helping a malicious user to modify the SQL query by injecting a specially crafted parameter value. This kind of flaw is also termed as ORM Injection. The latest version of Django however does not contain this flaw.

Second, Django has not implemented Query Parameterization and Escaping of characters for some of the querysets. This includes raw(), extra() and RawSQL. The application will be vulnerable to SQL injection if additional controls are not implemented by the developer.

Third, Django gives developers the ability to write SQL queries directly which will bypass the model layer all together. The application will be vulnerable to SQL injection if additional controls are not implemented by the developer.
How to prevent?

First of all we can start by identifying if there are any existing SQL injection related vulnerabilities in the Django version we are using or about to use. This check can be periodically conducted to ensure that any new vulnerability in the framework is identified and Django updated to a version that does not contain the vulnerability.

Second, the use of raw(), extra(), RawSQL and direct SQL query should be avoided as much as possible and should only be used if you cannot express your query using other queryset methods. If at all these needs to be used, escape the user provided input by using params and do not quote placeholders in the SQL string.

The below examples shows the correct implementation:

raw()

lname = 'Doe'

Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])

extra()

Entry.objects.extra(where=['headline=%s'], params=['Lennon'])

RawSQL

queryset.annotate(val=RawSQL("select col from sometable where othercol = %s", (someparam,)))

Direct SQL Query

from django.db import connection

def my_custom_sql(self):

    with connection.cursor() as cursor:

     cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])

        row = cursor.fetchone()

    return row

As in the above example use %s and not ‘%s’ within the SQL string.
How to detect?

SQL injection can be detected in two ways:

    Performing Source Code Security Review
    Performing Web Application Vulnerability Scanning
