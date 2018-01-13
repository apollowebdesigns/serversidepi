from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

while True:
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    print("pitch {0} roll {1} yaw {2}".format(pitch, roll, yaw))
    count = 0
    if pitch > 300:
        if count % 2 == 0:
            sense.set_pixel(2, 2, (0, 0, 0))
        else:
            sense.set_pixel(2, 2, (0, 0, 255))
        count++
        sense.set_pixel(4, 2, (0, 0, 255))
        sense.set_pixel(3, 4, (100, 0, 0))
        sense.set_pixel(1, 5, (255, 0, 0))
        sense.set_pixel(2, 6, (255, 0, 0))
        sense.set_pixel(3, 6, (255, 0, 0))
        sense.set_pixel(4, 6, (255, 0, 0))
        sense.set_pixel(5, 5, (255, 0, 0))