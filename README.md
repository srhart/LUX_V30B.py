# LUX_V30B.py
Micropython library for the DFRobot LUX V30B i2c

example:

''
from machine import I2C, Pin
import luxv30b

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
led = Pin(25, Pin.OUT)

sensor = luxv30b.LUXV30B(i2c)
sensor.check(i2c)

print(bin(sensor.get_conf()[0])[2:])

print(sensor.get_lux())
''
