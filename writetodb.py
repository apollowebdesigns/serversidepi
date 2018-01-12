from sense_hat import SenseHat
import pymysql.cursors

sense = SenseHat()
sense.clear()

try:
    temp = sense.get_temperature()
except Exception:
    print('error getting sensehat temperature')
string_temp = str(temp)
 

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='raspberry',
                             db='weather',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `temperature` (`temperature`) VALUES (%s)"
        cursor.execute(sql, (temp))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
finally:
    connection.close()