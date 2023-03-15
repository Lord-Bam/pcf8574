from machine import Pin, I2C
import time
import sh1106

# initialize
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)
i2c.writeto(56, b'\xfe')

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
        
def go_right():
    #get 4 lowest bits
    l_bits = i2c.readfrom(56, 1)
    l_bits = int.from_bytes(l_bits, 'big')
    l_bits = l_bits & 15
#     print("lowest bits", l_bits)
    
    #It needs a mask since bit operations are on ints and not 4 bits.
    #I invert since with bitshifting a 0 is inserted.
    l_bits = ~l_bits & 0xF
#     print("lowest bits inverted", l_bits)
    
    
    #shift lowest bits by 1.
    l_bits = l_bits << 1
#     print("lowest bits shifted", l_bits)
    if l_bits == 16:
        l_bits = 1
        print("reset")
    
    #It needs a mask since bit operations are on ints and not 4 bits.
#     print("lowest after possible reset", l_bits)
    l_bits = ~l_bits & 0xF
#     print("finel lowest bits", l_bits) 
    
    
    #Get 4 highest bits (there is something wrong here... can't figure it out.)
    #Problem is when a button is pressed the value 0 is written back and that messes everything up.
#     h_bits = i2c.readfrom(56, 1)
#     h_bits = int.from_bytes(h_bits, 'big')
#     h_bits = h_bits & 240
    
    number = l_bits + 240
    i2c.writeto(56, number.to_bytes(2, 'big'))
    return number

    
def go_left():
    pass


def print_byte(byte):
    i = int.from_bytes(byte, 'big') 
    bit_string = ('{:0>8}'.format(f"{i:b}"))
    return bit_string


print(i2c.scan())
inputs_pcf_before = -1



while True:
#     led = time.ticks_ms()//1000%4
#     print(led)
#     if read_bit(56, led) == 1:
#         write_bit(56, led, 0)

    go_right()
    byte = read_byte(56)
    print(print_byte(byte))
    
    for x in range(4,8):
        print("reading pin:",  x ,  read_bit(56, x))
    time.sleep(1)
    
    
    
#     time.sleep(1)
#     write_bit(56, 0, 1)
#     print(read_bit(56, 0))
# 
#     
#     time.sleep(1)
#     write_bit(56, 0, 0)
#     print(read_bit(56, 1))
#       
#     time.sleep(1)
#     write_byte(56, b'\xff')
#     
#     time.sleep(1)
#     write_byte(56, b'\xf0')
#     print(read_byte(56))
#     print(print_byte())

    