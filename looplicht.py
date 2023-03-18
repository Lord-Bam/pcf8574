from machine import Pin, I2C
import time
import sh1106
import machine

# initialize
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)
i2c.writeto(56, b'\xfe')
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


def print_byte(byte):
    i = int.from_bytes(byte, 'big') 
    bit_string = ('{:0>8}'.format(f"{i:b}"))
    return bit_string


def interrupt(self):
    print("interrupt")
    for x in range(4,8):
        print("reading pin:",  x ,  read_bit(56, x))


print(i2c.scan())
inputs_pcf_before = -1

def traite_interruption(self):
    print("interrupt")
    for x in range(4,8):
        print("reading pin:",  x ,  read_bit(56, x))

pin_interrupt = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
pin_interrupt.irq(trigger = machine.Pin.IRQ_FALLING, handler = interrupt)


while True:
    go_right()
    byte = read_byte(56)
    #print(print_byte(byte))
    

    time.sleep(1)

    