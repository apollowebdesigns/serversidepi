import psycopg2
from configparser import ConfigParser
import sys

from sense_hat import SenseHat
import datetime

sense = SenseHat()
sense.clear()

try:
    temp = sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
except Exception:
    print('error getting sensehat temperature')

# Getting data values
string_datetimenowlong = str(datetime.datetime.now().isoformat())
string_datetimenow = string_datetimenowlong[0:19]
string_temp = str(round(temp, 6))
string_pressure = str(round(pressure, 6))
string_humidity = str(round(humidity, 6))

## Connecting to database

conn = None

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db


def insert_vendor(date, temperature, pressure, humidity):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO data(date, temperature, pressure, humidity)
             VALUES(%s, %s, %s, %s) RETURNING date;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (date, temperature, pressure, humidity,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    return vendor_id

def insert_vendor_list(date, temperature, pressure, humidity):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO data(date, temperature, pressure, humidity)
             VALUES(%s, %s, %s, %s) RETURNING date;"""
    conn = None
    vendor_id = None
    try:
        print('the input values are %s, %s, %s, %s', date, temperature, pressure, humidity)
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (date, temperature, pressure, humidity,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print('function executed ok')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    return vendor_id

try:  
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print('what is the version??')
    print(ver)   

    insert_vendor(string_datetimenow, string_temp, string_pressure, string_humidity)

    print('added data correctly')
    

except psycopg2.DatabaseError as e:
    print(e)  
    sys.exit(1)
    
    
finally:
    if conn:
        conn.close()