import machine
import utime

pot = machine.ADC(26)
flex = machine.ADC(27)


while True:
    print(pot.read_u16(), flex.read_u16())
    utime.sleep(0.1)
