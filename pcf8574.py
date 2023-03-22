import machine

class Pcf8574:
    
    def __init__(self, input_output_pins, address, scl, sda, interrupt):
        self.io_pins = input_output_pins
        self.address = address
        
        self.i2c = machine.I2C(0, scl=machine.Pin(scl), sda=machine.Pin(sda), freq=400000)
        self.i2c.writeto(self.address, b'\xff')
        self.mask = 0
        for x in range(8):
            if input_output_pins[x] == "i":
                self.mask = self.mask + 2**x
        print("mask", self.mask)
        
        
    def read_byte(self):
        byte = self.i2c.readfrom(self.address, 1)
        return byte

        
    def read_bit(self, bit):
        byte = self.i2c.readfrom(self.address, 1)
        return (byte[0] >> bit ) & 1
    
    def write_byte(self, byte):
        self.i2c.writeto(self.address, byte)
        byte = self.i2c.readfrom(self.address, 1)
        return byte
    
    
    def write_bit(self, bit, value):
        #get the old value.
        byte = self.i2c.readfrom(self.address, 1)
        
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
                byte = byte | self.mask
                self.i2c.writeto(self.address, byte.to_bytes(2, 'big'))
                byte = self.i2c.readfrom(self.address, 1)
                return byte
            
            else:
                #switch off pin.
                value = 1 << bit
                byte = byte[0] + value
                 #since pin 4 --> 7 have to remain 1, we or 240 to it. (top 4 bits)
                byte = byte | self.mask
                self.i2c.writeto(self.address, byte.to_bytes(2, 'big'))
                byte = self.i2c.readfrom(self.address, 1)
                return byte
            
    def pcf_pretty_print(self):
        byte = self.i2c.readfrom(self.address, 1)
        i = int.from_bytes(byte, 'big') 
        bit_string = ('{:0>8}'.format(f"{i:b}"))
        return bit_string

        

    