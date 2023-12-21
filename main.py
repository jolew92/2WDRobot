#Include the library files
from machine import Pin,PWM
import time

servo = PWM(Pin(0))#Include the servo motor pin
servo.freq(50)#Set the frequency

Trig = Pin(14,Pin.OUT)#Include the Trig pin
Echo = Pin(15,Pin.IN)#Include the Echo pin

#Motor driver pins
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(5, Pin.OUT)
IN4 = Pin(4, Pin.OUT)


def forward():
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()
    
def backward():
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()
    
def left():
    IN3.low()
    IN4.low()
    IN1.low()
    IN2.high()
    
def right():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.high()

def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()
    
#Get the distance
def distance():
    low = 0
    high = 0
    Trig.value(0)
    time.sleep_us(4)
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
      
    while Echo.value() == 0:
       low = time.ticks_us()
       
    while Echo.value() == 1:
       high = time.ticks_us()
       
    
    print(low)
    print(high)
       
    t = high - low
    cm = t/29/2#Time convert to the cm
#     time.sleep(0.1)
    return cm

def servoLeft():
    servo.duty_u16(6000) #1500-8500
    
def servoRight():
    servo.duty_u16(2000) #1500-8500
    
def servoStart():
    servo.duty_u16(4000) #1500-8500

while True:
    dis = distance()
    print("Distance:", dis)
    
    if 7 < dis <= 15:
        print("Obstacle detected!")
        stop()
        time.sleep(0.1)
        
        servoLeft()
        time.sleep(0.1)
        leftDis = distance()
        print("Left Distance:", leftDis)
        time.sleep(0.1)
        
        servoStart()
        time.sleep(0.1)
        
        servoRight()
        time.sleep(0.1)
        rightDis = distance()
        print("Right Distance:", rightDis)
        time.sleep(0.1)
        
        servoStart()
        time.sleep(0.1)
        
        if leftDis > rightDis:
            print("Turn Left")
            left()
            time.sleep(0.5)
        elif leftDis < rightDis:
            print("Turn Right")
            right()
            time.sleep(0.5)
        
        forward()
        time.sleep(0.1)
    elif dis < 7:
        print("Move Backward")
        backward()
        time.sleep(0.5)
        stop()
        time.sleep(0.1)
    elif dis > 15:
        print("Moving forward.")
        forward()
        time.sleep(0.1)
    elif dis < 2:
        print("Error")
        stop()
        time.sleep(1)
