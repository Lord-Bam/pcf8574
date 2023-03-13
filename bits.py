from machine import Pin, I2C
import time
# https://realpython.com/python-bitwise-operators/
#https://www.guru99.com/python-string-format.html

number = 128
# f"{a:b}" --> print a in binary format
# {:0>8}
# 0 = padding character
# > allign right
# 8 --> string of 8 long
bit_string = ('{:0>8}'.format(f"{number:b}"))
print(bit_string)

print(bin(10))

print((7 & 3).to_bytes(1, "big"))


number = number | (1 << 0)
print(number)

value = (1 << 7)
print("value", value)


i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)

i2c.writeto(56, b'\xff')
byte = i2c.readfrom(56, 1)
print(byte)
time.sleep(1)


byte = hex(255)
print(str(byte))

i2c.writeto(56, str(byte))
byte = i2c.readfrom(56, 1)
print(byte)

value = 1 << 0
test = bytearray(1)
test[0] = value & 0xff
i2c.writeto(56, test)

value = 1 << 3
test[0] = value & 0xff
i2c.writeto(56, test)

i2c.writeto(56, str(byte))
byte = i2c.readfrom(56, 1)
print(byte)

value = 1 << 3
print(1 << 2)
print(test[0])
test[0] = value & 0xff
i2c.writeto(56, test)






