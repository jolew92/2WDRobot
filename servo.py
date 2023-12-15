import time
from machine import Pin, PWM
import random

class ServoScanner:
    def __init__(self, pin, min_duty, max_duty, calibration, scan_speed=700, pause_time=0.5):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.middle_duty = (min_duty + max_duty) // 2
        self.calibration = calibration
        self.scan_speed = scan_speed
        self.pause_time = pause_time
        self.last_rotation_stage = 1

    def scan_area(self, start, end, direction):
        if direction == '-':
            speed = -self.scan_speed
        else:
            speed = self.scan_speed
        
        for duty_cycle in range(start, end, speed):
            self.pwm.duty_u16(duty_cycle)
            time.sleep_ms(50)  # Krótka pauza między krokami
            
    def reset(self):
        self.pwm.duty_u16(self.middle_duty - self.calibration)
        print("middle")
            
    def step(self, rotation_stage=None):
        if rotation_stage == None: rotation_stage = self.last_rotation_stage
        if rotation_stage == 1:
            self.scan_area(self.middle_duty, self.min_duty, '-')  # Skanuj w lewo do MIN_DUTY
            self.last_rotation_stage = 2
        elif rotation_stage == 2:
            self.scan_area(self.min_duty, self.middle_duty, '+')  # Skanuj w prawo do MIDDLE_DUTY
            self.last_rotation_stage = 3
        elif rotation_stage == 3:
            self.scan_area(self.middle_duty, self.max_duty, '+')  # Skanuj w prawo do MAX_DUTY
            self.last_rotation_stage = 4
        elif rotation_stage == 4:
            self.scan_area(self.max_duty, self.middle_duty - self.calibration, '-')  # Skanuj w lewo do MIDDLE_DUTY - CALIBRATION
            self.last_rotation_stage = 1

    def perform_scan(self):
        self.scan_area(self.middle_duty, self.min_duty, '-')  # Skanuj w lewo do MIN_DUTY
        time.sleep(self.pause_time)  # Pauza
        
        self.scan_area(self.min_duty, self.middle_duty, '+')  # Skanuj w prawo do MIDDLE_DUTY
        time.sleep(self.pause_time)  # Pauza
        
        self.scan_area(self.middle_duty, self.max_duty, '+')  # Skanuj w prawo do MAX_DUTY
        time.sleep(self.pause_time)  # Pauza
        
        self.scan_area(self.max_duty, self.middle_duty - self.calibration, '-')  # Skanuj w lewo do MIDDLE_DUTY - CALIBRATION
        time.sleep(self.pause_time)  # Pauza