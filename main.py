from machine import Pin, I2C
import time
import sh1106

# initialize
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)
i2c.writeto(56, b'\xff')

def read_byte(address):
    byte = i2c.readfrom(address, 1)
    return byte

def read_bit(adress, bit):
    byte = i2c.readfrom(adress, 1)
    return (byte[0] >> bit ) & 1
    
def write_byte(address, byte):
    byte = i2c.writeto(address, byte)
    return byte


def write_bit(adress, bit, value):
    byte = i2c.readfrom(56, 1)
    
    old_value = (byte[0] >> bit ) & 1
    
    if old_value == value:
        return byte
    
    else:
        if value == 0:
            value = 1 << bit
            byte = byte[0] - value
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            return byte
        
        else:
            value = 1 << bit
            byte = byte[0] + value
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            return byte





print(i2c.scan())
inputs_pcf_before = -1

while True:
    time.sleep(1)
    write_bit(56, 0, 1)
    print(read_bit(56, 0))
    
    time.sleep(1)
    write_bit(56, 0, 0)
    print(read_bit(56, 1))
      
    time.sleep(1)
    write_byte(56, b'\xff')
    
    time.sleep(1)
    write_byte(56, b'\xf0')
    print(read_byte(56))

    