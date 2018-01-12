import MySQLdb as my
from sense_hat import SenseHat

db = my.connect(host="127.0.0.1",
user="root",
passwd="raspberry",
db="weather"
)

sense = SenseHat()
sense.clear()

try:
    temp = sense.get_temperature()
except Exception:
    print('error getting sensehat temperature')
string_temp = str(temp)
 
cursor = db.cursor()
 
sql = "insert into temperature VALUES(" + string_temp + ")"
 
number_of_rows = cursor.execute(sql)
db.commit()   # you need to call commit() method to save 
              # your changes to the database
 
 
db.close()