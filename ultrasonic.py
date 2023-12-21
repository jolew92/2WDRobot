from machine import Pin, time_pulse_us
import time

SOUND_SPEED=340 
TRIG_PULSE_DURATION_US=10

trig_pin = Pin(14, Pin.OUT) 
echo_pin = Pin(15, Pin.IN)  

while True:
    trig_pin.value(0)
    time.sleep_us(5)
    trig_pin.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    trig_pin.value(0)

    ultrason_duration = time_pulse_us(echo_pin, 1, 30000)
    distance_cm = SOUND_SPEED * ultrason_duration / 20000

    print(f"Distance : {distance_cm} cm")
    time.sleep_ms(500)