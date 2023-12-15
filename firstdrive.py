from machine import Pin, PWM
from time import sleep

IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(5, Pin.OUT)
IN4 = Pin(4, Pin.OUT)

#speed = PWM(Pin(4))
#speed.freq(1000)
sleep(3)

for i in range(0,5):
#        speed.duty_u16(10000)
        IN1.low()  #spin forward
        IN2.high()
        IN3.low()  #spin forward
        IN4.high()
        sleep(3)
        
        IN1.low()  #stop
        IN2.low()
        IN3.low()  #stop
        IN4.low()
        sleep(1)
        
        IN1.high()  #spin backward
        IN2.low()
        IN3.high()  #spin backward
        IN4.low()
        sleep(3)
        
        IN1.low()  #stop
        IN2.low()
        IN3.low()  #stop
        IN4.low()
        sleep(1)
        