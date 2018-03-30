import psycopg2
import sys


con = None

try:  
    con = psycopg2.connect("dbname=weather user=postgres password=postgres")
    cur = con.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print('what is the version??')
    print(ver)   
    

except psycopg2.DatabaseError as e:
    print(e)  
    sys.exit(1)
    
    
finally:
    if con:
        con.close()