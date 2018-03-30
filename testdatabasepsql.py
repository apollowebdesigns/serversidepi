import psycopg2
import sys


conn = None

try:  
    conn = psycopg2.connect(host="localhost",database="weather", user="postgres", password="postgres")
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