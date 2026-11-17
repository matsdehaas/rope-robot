"""
Group Members: Mats de Haas

Date: 18/09/202
 
Brick Number: 3

Lab Number: 1

Problem Number: 5
 
Brief Program/Problem Description: 

    Create a braitenberg vehicle, that reacts to light either in a cowardly manner
    or an aggressive manner. 

Brief Solution Summary:

	For this solution, we took input from the color sensors set to ambient light
    mode. Some basic functions were made to help with reading light, converting it
    to a speed percentage based on a gain variable, and limiting that speed to a
    maximum speed (in this case 100%). Finally, the method run_behavior runs a
    terminal menu in which either of the 2 emotions can be chosen. Based on the
    choice, the input from the sensors will be mapped in different ways to 
    display the chosen emotion.


Used Resources/Collaborators:
	...

I hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""


#!/usr/bin/env python3
from time import sleep

import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor

wheel_diameter_mm = 56.1 #mm
axle_length = 112/ 10 # cm # 112mm from middle # 85mm inner edges #
wheel_circ = (wheel_diameter_mm / 10) * math.pi # cm.
circumference = axle_length * math.pi
rot_per_revolution = circumference / wheel_circ

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
right_motor = LargeMotor(OUTPUT_B)
left_motor = LargeMotor(OUTPUT_A)
gyro = GyroSensor()
cs_left = ColorSensor(INPUT_3)
cs_right = ColorSensor(INPUT_2)
cs_left.mode  = 'COL-AMBIENT'
cs_right.mode = 'COL-AMBIENT'

def limit(x, lo, hi):
    return max(lo, min(hi, x))

def convert(v, gain=4):
    return limit(gain * v, 0, 100)

def read_light():
    return cs_left.ambient_light_intensity, cs_right.ambient_light_intensity

def run_behavior(behavior, gain=4, threshold=10):
    print("Behavior:", behavior, "(press ctrl C in terminal to stop)")
    try:
        while 1:
            L, R = read_light()

            left_speed = right_speed = 0

            if L >= threshold or R >= threshold:
                if behavior == 'aggression':
                    left_speed  = -convert(R, gain)
                    right_speed = -convert(L, gain)
                elif behavior == 'coward':
                    left_speed  = convert(L, gain)
                    right_speed = convert(R, gain)

            tank_drive.on(SpeedPercent(left_speed), SpeedPercent(right_speed))

            # Print debug info
            print("L={:>3}  R={:>3}  |  Left motor={:>3.0f}%  Right motor={:>3.0f}%"
                  .format(L, R, left_speed, right_speed))

            sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        tank_drive.off()
        print("Stopped.")

while 1:
  print('''
  ------------------------
  Activities:
  braitenberg
  ------------------------
  ''')
  activity = input("Enter activity: ")
  if (activity == "braitenberg"):
     print("Braitenberg demo. Choose behavior:")
     print("1 = Cowardice   2 = Aggression")
     choice = input("Select (1/2): ").strip()

     if choice == "1":
        input("Press Enter to start cowardice... (stop with Enter)")
        run_behavior('coward')
     elif choice == "2":
        input("Press Enter to start aggression... (stop with Enter)")
        run_behavior('aggression')
     else:
        print("Unknown choice.")
        tank_drive.off()