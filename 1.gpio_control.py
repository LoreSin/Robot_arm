import tkinter as tk
import RPi.GPIO as GPIO
from gpioclass import Motor


# motor setting
GPIO.setmode(GPIO.BCM)
motor_base = Motor(22,23) # Base Axis(Left or Right)
motor_shoulder = Motor(24,25) # Shoulder
motor_wrist = Motor(17,18) # Wrist
motor_gripper = Motor(5,13) # gripper



# UI 
root = tk.Tk()

btn_up = tk.Button(root, text='up')
btn_up['command'] = lambda : motor_shoulder.run('right', 0.5)
btn_up.grid(row=1,column=2, sticky=tk.NSEW)
btn_down = tk.Button(root, text='down')
btn_down['command'] = lambda : motor_shoulder.run('left', 0.5)
btn_down.grid(row=3,column=2, sticky=tk.NSEW)



btn_left = tk.Button(root, text='left')
btn_left['command'] = lambda : motor_base.run('left', 0.5)
btn_left.grid(row=2,column=1, sticky=tk.NSEW)
btn_right = tk.Button(root, text='right')
btn_right['command'] = lambda : motor_base.run('right', 0.5)
btn_right.grid(row=2,column=3, sticky=tk.NSEW)
btn_stop = tk.Button(root, text='stop')
btn_stop['command'] = lambda : motor_base.run('stop')
btn_stop.grid(row=2,column=2, sticky=tk.NSEW)

exit_btn = tk.Button(root, text='quit', command=root.destroy)
exit_btn.grid(row=4,column=0, sticky=tk.NSEW)



# Gui Functions

def key_functions(event):
    print(event.keycode)
    if event.keycode == 25: # W key
        motor_shoulder.run('right', 0.2)
    elif event.keycode == 38: # A key
        motor_base.run('left', 0.5)
    elif event.keycode == 39: # S key
        motor_shoulder.run('left', 0.2)
    elif event.keycode == 40: # D key
        motor_base.run('right', 0.5)
    elif event.keycode == 65: # Space key
        pass
    elif event.keycode == 56: # B key
        pass


    elif event.keycode == 32: # O key
        motor_gripper.run('right', 0.2)
    elif event.keycode == 33: # P key
        motor_gripper.run('left', 0.2)

    elif event.keycode == 31: # I key
        motor_wrist.run('right', 0.5)
    elif event.keycode == 44: # J key
        motor_wrist.run('left', 0.5)

    elif event.keycode == 24: # Q key
        root.destroy()


root.bind('<KeyPress>', key_functions)
#root.geometry('400x400')
root.settitle('Robot Controller')
root.mainloop()



motor_base._stop()
motor_shoulder._stop()
GPIO.cleanup()

