import psycopg2
from configparser import ConfigParser
import sys


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
    

except psycopg2.DatabaseError as e:
    print(e)  
    sys.exit(1)
    
    
finally:
    if conn:
        conn.close()