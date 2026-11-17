"""
Group Members: Aemad Qamar, Mats de Haas

Date: 16/09/2025
 
Brick Number: 3

Lab Number: 1

Problem Number: 2
 
Brief Program/Problem Description: 

	The problem at hand is to gather data about the difference between the desired 
  and inputted movement, and the actual result of the robots movement.

Brief Solution Summary:

	We created simple methods to both drive the robot straight for a certain distance
  and turn in place. To translate the input degrees of rotation we used the axle length
  to calculate the circumfurance of the circle the robot would drive on if it were to turn
  in place. We then calculated the amount of rotations it would take to turn 360
  degrees. The required rotations can then be achieved by deviding it by 360 and
  multiplying it by that number.
  We also made a function to translate the motor position degrees
  to a distance in cm, based on the circumference of the wheels. 
  Finally, we wrote functions that take a certain desired distance or rotation,
  send that to the robot, and returns the actual movement registered from either
  the motor sensors or the gyro sensor, as well as the difference (error).

Used Resources/Collaborators:
	...

We hereby certify that I/we have produced the following solution 
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

def drive_straight(distance_cm, speed=25):

  tank_drive.off

  rotations = distance_cm / wheel_circ

  tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)

def turn(angle, speed=15):

  tank_drive.off
  fraction = angle / 360.0

  rotations = rot_per_revolution * fraction

  tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(-speed), rotations)


def rotation_test(target_angle, speed=15): #angle should be less than 360 degrees for meaningfull tests

  gyro.reset()

  turn(target_angle, speed)

  measured_angle = gyro.angle
  error_angle = target_angle - measured_angle

  print("Target angle: {}".format(target_angle))
  print("Measured angle: {}".format(measured_angle))
  print("Error: {}".format(error_angle))
  print("Motor L: {}, Motor R: {}".format(left_motor.position, right_motor.position))

  return error_angle

def degrees_to_cm(degrees):
  return (degrees / 360.0) * wheel_circ

def straight_line_test(distance_cm=10, speed=25):
  initial_Lpos = left_motor.position
  intial_Rpos =right_motor.position
  drive_straight(distance_cm, speed)

  end_left = left_motor.position -initial_Lpos
  end_right = right_motor.position -intial_Rpos

  distance_left = degrees_to_cm(end_left)
  distance_right = degrees_to_cm(end_right)
  avg_distance = (distance_left + distance_right) / 2

  error_distance = distance_cm - avg_distance
  error_drift = distance_left - distance_right

  print("Target: {:.2f} cm".format(distance_cm))
  print("Left: {:.2f} cm, Right: {:.2f} cm".format(distance_left, distance_right))
  print("Avg: {:.2f} cm".format(avg_distance))
  print("Error distance: {:.2f} cm".format(error_distance))
  print("Error drift (L-R): {:.2f} cm".format(error_drift))

  return error_distance, error_drift


while 1:
  print('''
  ------------------------
  Activities:
  rotation_test
  straight_line_test
  drive_straight
  turn
  ------------------------
  ''')
  activity = input("Enter activity: ")
  if (activity == "rotation_test"):
    rotation_test(int(input("Rotation in degrees: ")))
  elif (activity == "straight_line_test"):
    straight_line_test(int(input("Distance(cm): ")))
  elif (activity == "drive_straight"):
    drive_straight(int(input("Distance(cm): ")))
  elif (activity == "turn"):
    turn(int(input("Angle (degrees): ")))