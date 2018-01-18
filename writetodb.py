from sense_hat import SenseHat
import pymysql.cursors
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
string_datetimenow = str(datetime.datetime.now().isoformat())
string_temp = str(temp)
string_pressure = str(pressure)
string_humidity = str(humidity)

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
        sql = "INSERT INTO `temperature` (`string_datetimenow`) (`temperature`) (`pressure`) (`humidity`) VALUES "+ string_datetimenow + " " + temp + " "+ pressure + " " + humidity + " "
        cursor.execute(sql, (string_datetimenow, temp, pressure, humidity))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
finally:
    connection.close()