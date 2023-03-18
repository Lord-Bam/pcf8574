from machine import Pin, I2C
from time import sleep
from sh1106 import SH1106_I2C

# construct a hardware I2C bus
i2c = I2C(0, scl=Pin(23), sda=Pin(22), freq=400000)

oled = SH1106_I2C(128, 64, i2c, rotate=180)

print(i2c.scan())

def pcf_pins_naar_s_bin(pcf_pins):
    pcf_pins >> 4
    s1_s4 = bin(pcf_pins)[6:]
    print(s1_s4)
    return s1_s4

def send_to_oled(lines):
    oled.fill(0)
    line_nr = 0
    for line in lines:
        oled.text(line, 0, line_nr * 10)
        line_nr += 1
    oled.show()
    

def send_to_pcf(byte):
    x = bytearray(1)
    x[0] = byte
    i2c.writeto(56,x)  # https://mpython.readthedocs.io/en/master/library/micropython/machine/machine.I2C.html
    
inputs_pcf_vorige = 0b11111111

#led 1,2,3,4 aan P3 P2 P1 P0 en S 1,2,3,4 aan pinnen P4,5,6,7'

while True:
    
    inputs_pcf =  i2c.readfrom(56, 1)
    inputs_pcf_int = int.from_bytes(inputs_pcf, 'big')  # byte string buvffer naar gewone integer omzetten
    
    if inputs_pcf_int != inputs_pcf_vorige:
        byte_to_send = (inputs_pcf_int >> 4) | 0b11110000  # schakelaars aan pinnen 7-4 naar leds aan pinnen 3-0 schuiven en pinnen  7-4  "1" maken met OR
        send_to_pcf(byte_to_send)
        send_to_oled(["leds-schak",bin(byte_to_send),pcf_pins_naar_s_bin(byte_to_send),"RP2 CVO FOCUS"])
        
        
# import machine
# import sh1106
#from ssd1306 import SSD1306_I2C


# oled.fill(0)
# oled.text("Hello World!", 0, 0)
# oled.show()

        
        
        