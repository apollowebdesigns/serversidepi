# Flask Raspberry Pi Repo

Uses nanpy to control motors with a slave arduino

## Installing with virtualenv

```
sudo python3 -m pip install virtualenv
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt 
```

## Starting up the application

Use cron to run the application via startapp.py
```
...
...
@reboot /home/pi/Documents/serversidepi/app.py >/home/pi/logs/pythonlog 2>&1
```

## Starting the camera

Create a file in
```
/etc/init.d
```

For example
```
/etc/init.d/superscript
```

place the startup of the camera inside the superscript e.g.
```
sh /home/pi/Documents/RPi_Cam_Web_Interface/start.sh >/home/pi/logs/cameralog 2>&1
```

## Use python with git

A cool toy!

[GitPython](https://github.com/gitpython-developers/GitPython)

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

## Server sent event information

Always prefix a sse response with:

```
'data: insert a random string'
```