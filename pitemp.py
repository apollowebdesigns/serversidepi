import os

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("'C\n", "")
        temp = temp.replace("temp=","")
        return float(temp)