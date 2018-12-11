import os
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("'C\n", "")
        temp = temp.replace("temp=","")
        return float(temp)

def get_sensor_data():
        sense.clear()
        o = sense.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]
        yaw = o["yaw"]
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        return {
                pitch: pitch,
                roll: roll,
                yaw: yaw,
                pressure: pressure,
                temp: temp,
                humidity: humidity
        }

def get_all_data():
        all_data = get_sensor_data()
        all_data['pitemp'] = measure_temp()
        return all_data