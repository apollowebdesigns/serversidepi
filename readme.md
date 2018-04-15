# Flask Raspberry Pi Repo

Uses nanpy to control motors with a slave arduino

## Logging in with MySQL

use command 
<code>mysql -p -u root</code>

and then type in the desired password

### Mock databases

weather

## Database readme info

https://github.com/PyMySQL/PyMySQL this is your bible!!!

## Using Postgres

connect to database in postgres shell
\c weather 

delete first few records

DELETE FROM data;

## SQL used to create database

<code>
create table data (date varchar(20), temperature varchar(20), pressure varchar(20), humidity varchar(20));
</code>

## Database more info

http://pymysql.readthedocs.io/en/latest/user/examples.html

## Machine learning tutorial for raspberry pi

TOTO: integrate this

https://www.pyimagesearch.com/2017/12/18/keras-deep-learning-raspberry-pi/