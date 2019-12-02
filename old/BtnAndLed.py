import RPi.GPIO as GPIO
import time


switch_pin = 4 # BCM pin 4, BOARD pin 7
led_pin = 18
def main():
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(switch_pin, GPIO.IN)  # Switch
    GPIO.setup(led_pin, GPIO.OUT)  # Switch
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            value = GPIO.input(switch_pin)
            if value != prev_value:
                if value == GPIO.HIGH:
                    value_str = "HIGH and LED ON"
                    GPIO.output(led_pin, GPIO.HIGH)
                else:
                    value_str = "LOW and LED OFF"
                    GPIO.output(led_pin, GPIO.LOW)
                print("Value read from pin {} : {}".format(switch_pin,
                                                           value_str))
                prev_value = value
            time.sleep(.05)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
