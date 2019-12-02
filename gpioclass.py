import RPi.GPIO as GPIO
import time

# need to set mode with BCM (Raspberry PI Pinmap)
# GPIO.setmode(GPIO.BCM)


class Motor:
    All = []
    def __init__(self, right_pin, left_pin, name=None):
         self.right_pin = right_pin
         self.left_pin = left_pin
         GPIO.setup(self.right_pin, GPIO.OUT)
         GPIO.setup(self.left_pin, GPIO.OUT)
         if name:
             self.name = name
         Motor.All.append(self)

    def _left(self):
         GPIO.output(self.right_pin, GPIO.LOW)
         GPIO.output(self.left_pin, GPIO.HIGH)

    def _right(self):
         GPIO.output(self.left_pin, GPIO.LOW)
         GPIO.output(self.right_pin, GPIO.HIGH)

    def _stop(self):
         GPIO.output(self.left_pin, GPIO.LOW)
         GPIO.output(self.right_pin, GPIO.LOW)

    def _break(self):
         GPIO.output(self.left_pin, GPIO.HIGH)
         GPIO.output(self.right_pin, GPIO.HIGH)

    def run(self, direction='stop', second=0.1):
        try:
            if direction =='right':
                self._right()
            elif direction =='left':
                self._left()
            elif direction =='break':
                self._break()
                return
            time.sleep(second)
            self._stop()
            time.sleep(0.05)
        except e:
            self._stop()



if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    motor = Motor(22,23)
    try:
        while True:
            motor.run('right')
            motor.run('left')
            motor.run('right')
            motor.run('left')
    finally:
        motor.run()
        GPIO.cleanup()



