from machine import Pin, I2C
import time
import sh1106
import machine

# initialize
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)
i2c.writeto(56, b'\xff')
#i2c.writeto(56, 0b11111110) this is the same as above.


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
    #get the old value.
    byte = i2c.readfrom(56, 1)
    
    #Did the pin change value?
    old_value = (byte[0] >> bit ) & 1
    if old_value == value:
        return byte
    
    
    else:
        #switch on pin.
        if value == 0:
            value = 1 << bit
            byte = byte[0] - value
            #since pin 4 --> 7 have to remain 1, we or 240 to it. (top 4 bits)
            byte = byte | 240
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            return byte
        
        else:
            #switch off pin.
            value = 1 << bit
            byte = byte[0] + value
             #since pin 4 --> 7 have to remain 1, we or 240 to it. (top 4 bits)
            byte = byte | 240
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            return byte


def parse_byte(byte):
    i = int.from_bytes(byte, 'big') 
    bit_string = ('{:0>8}'.format(f"{i:b}"))
    return bit_string


def interrupt(self):
    #check the 4 top pins.
    for x in range(4,8):
        if read_bit(56, x) == 0:
            #x - 4 --> button 1 on pin 4 becomes pin 0
            #"1 - read_bit(56, x - 4)" --> invert the 1.
            write_bit(56, x - 4, 1 - read_bit(56, x - 4))

print(i2c.scan())
inputs_pcf_before = -1


pin_interrupt = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
pin_interrupt.irq(trigger = machine.Pin.IRQ_FALLING, handler = interrupt)


while True:
    time.sleep(1)

    