from machine import Pin
import utime
from micropython_ir.ir_rx.nec import NEC_8
import servo

class CarController:
    def __init__(self):
        self.pressedButton = -1
        self.action = 'Stop'  # Początkowa akcja to 'Stop'

        # Car
        # Left wheel
        self.IN1 = Pin(2, Pin.OUT)
        self.IN2 = Pin(3, Pin.OUT)
        # Right wheel
        self.IN3 = Pin(5, Pin.OUT)
        self.IN4 = Pin(4, Pin.OUT)

        # Utwórz instancję IR odbiornika z odpowiednim callbackiem
        ir = NEC_8(Pin(8, Pin.IN), self.callback)
        
        # Servo
        self.servo_controller = servo.ServoScanner(pin=0, min_duty=1000, max_duty=9000, calibration=700)

    def callback(self, data, addr, ctrl):
        if data < 0:  # NEC protocol sends repeat codes.
            pass
        else:
            self.pressedButton = data

        if self.pressedButton == 24:
            self.action = 'Forward'
            print('Forward')
        elif self.pressedButton == 82:
            self.action = 'Backward'
            print('Backwards')
        elif self.pressedButton == 8:
            self.action = 'Left'
            print('Left')
        elif self.pressedButton == 90:
            self.action = 'Right'
            print('Right')
        elif self.pressedButton == 28:
            self.action = 'Stop'
            print('Stop')
        else:
            print('Not defined:' + str(self.pressedButton))

    def run(self):
        while True:
            # Uruchom logikę sterowania samochodem na podstawie akcji
            if self.action == 'Forward':
                self.IN1.low()
                self.IN2.high()
                self.IN3.low()
                self.IN4.high()
                self.servo_controller.step()
            elif self.action == 'Backward':
                self.IN1.high()
                self.IN2.low()
                self.IN3.high()
                self.IN4.low()
                self.servo_controller.step()
            elif self.action == 'Left':
                # Zatrzymaj prawe koło
                self.IN3.low()
                self.IN4.low()
                # Ruszaj lewym kołem
                self.IN1.low()
                self.IN2.high()
                self.servo_controller.step(1)
            elif self.action == 'Right':
                 # Zatrzymaj lewe koło
                self.IN1.low()
                self.IN2.low()
                # Ruszaj prawym kołem
                self.IN3.low()
                self.IN4.high()
                self.servo_controller.step(3)
            elif self.action == 'Stop':
                print('Stop')
                self.IN1.low()
                self.IN2.low()
                self.IN3.low()
                self.IN4.low()  
                self.servo_controller.reset()
            self.action = 'Stop'
            #self.servo_controller.reset()
            utime.sleep_ms(100)