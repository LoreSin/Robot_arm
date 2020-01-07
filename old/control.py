import RPi.GPIO as GPIO
from gpioclass import Motor


# motor setting
GPIO.setmode(GPIO.BCM)
motor_base = Motor(22,23) # Base Axis(Left or Right)
motor_shoulder = Motor(24,25) # Shoulder
motor_wrist = Motor(17,18) # Wrist
motor_gripper = Motor(5,13) # gripper


grip_object = lambda : motor_gripper.run('left', 1.5)
release_object = lambda : motor_gripper.run('right', 1.5)

def get_object(mode=None):
    '''
    object grip or release
    '''
    if mode in ['up', 'down'] == False:
        print('irregular command : functions get_object(mode=None)')
        return

    if mode == 'up':
        motor_shoulder.run('left', 2)
        grip_object()
        motor_shoulder.run('right', 3)
    elif mode == 'down':
        motor_shoulder.run('left', 1.8)
        release_object()
        motor_shoulder.run('right', 2.3)

def move_to_red_area():
    '''
    get object and move right area
    '''

    get_object('up')
    motor_base.run('right', 3.5)
    release_object()
    motor_base.run('left', 3.2)

def move_to_blue_area():
    '''
    get object and move left area
    '''

    get_object('up')
    motor_base.run('left', 2.5)
    release_object()
    motor_base.run('right', 3)

def clean_GPIO():
    motor_base._stop()
    motor_shoulder._stop()
    motor_wrist._stop()
    motor_gripper._stop()
    GPIO.cleanup()

if __name__ == "__main__":
    print()
    clean_GPIO()
