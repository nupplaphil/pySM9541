import time

from SM9541 import *

sensor = SM9541()

values = sensor.read_all()

while True:
    print(('Pressure   = {0:0.2f} cmH20'.format(values[1])))
    print(('Temp       = {0:0.3f} deg C'.format(values[2])))
    time.sleep(1)
