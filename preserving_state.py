from machine import Pin, I2C
import time

#initialize:
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)
i2c.writeto(56, b'\xff')


#get and save currents state
byte = i2c.readfrom(56, 1)
print("start state", byte)


#switch on led 1
time.sleep(0.3)
value = 1 << 0
byte = byte[0] - value
i2c.writeto(56, byte.to_bytes(2, 'big'))


time.sleep(0.3)
byte = i2c.readfrom(56, 1)
value = 1 << 1
byte = byte[0] - value
i2c.writeto(56, byte.to_bytes(2, 'big'))


time.sleep(0.3)
byte = i2c.readfrom(56, 1)
value = 1 << 2
byte = byte[0] - value
i2c.writeto(56, byte.to_bytes(2, 'big'))


time.sleep(0.3)
byte = i2c.readfrom(56, 1)
value = 1 << 3
byte = byte[0] - value
i2c.writeto(56, byte.to_bytes(2, 'big'))


time.sleep(0.3)
byte = i2c.readfrom(56, 1)
value = 1 << 3
byte = byte[0] + value
i2c.writeto(56, byte.to_bytes(2, 'big'))


# 
# time.sleep(0.3)
# byte = i2c.readfrom(56, 1)
# print("state", byte)
# 
# value = 1 << 0
# test[0] = (value | int.from_bytes(byte, 'big'))
# print(test[0])
# i2c.writeto(56, test)
# byte = i2c.readfrom(56, 1)
# print("state", byte)
