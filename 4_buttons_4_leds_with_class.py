import machine
import pcf8574
import time

print(5**2)

def interrupt_handler(Pin):
    time.sleep(0.1)
    print("button pressed")
    for pin in pcf.get_pins():
        if pin.get_state() != pin.get_previous_state() and pin.get_io() == "i":
            pin.set_previous_state(pin.get_state())
            switch_on_led(pin)
            
            
def switch_on_led(pin):
    pcf.write_bit(pin.get_pin_nr() - 4, pin.get_state())
    print(pcf.pcf_pretty_print())
        
    


io_pins = ["o","o","o","o","i","i","i","i"]
pcf = pcf8574.Pcf8574(io_pins, 56, 23, 22, 19, interrupt_handler)


# print(pcf.read_byte())
# print(pcf.read_bit(1))
# # print(pcf.write_byte(b'\x00'))
# print(pcf.write_bit(0, 0))
# print(pcf.write_bit(3, 0))
# print(pcf.pcf_pretty_print())


while True:
    pass
    