"""
Group Members: Mats de Haas, Aemad Qamar

Date: 17/09/2025
 
Brick Number: 3

Lab Number: 1

Problem Number: 3 
 
Brief Program/Problem Description: 

	Make the robot move in a square and a lemniscate shape. 

Brief Solution Summary:

  Algorithmic idea, underlying theory, etc...

Used Resources/Collaborators:
	...

I/we hereby certify that I/we have produced the following solution 
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
#   left_motor.position = 0
#   right_motor.position = 0

  turn(target_angle, speed)

  measured_angle = gyro.angle
  error_angle = target_angle - measured_angle

  print("Target angle: {}".format(target_angle))
  print("Measured angle: {}".format(measured_angle))
  print("Error: {}".format(error_angle))
  print("Motor L: {}, Motor R: {}".format(left_motor.position, right_motor.position))

  return error_angle

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

def rectangle(numTimes):
  for i in range(numTimes):
    straight_line_test(15)
    rotation_test(90)
    straight_line_test(15)
    rotation_test(90)
    straight_line_test(15)
    rotation_test(90)
    straight_line_test(15)
    rotation_test(90)

def rectangle_gyro(numTimes):
  for i in range(numTimes):
    straight_line_test(15)
    turn_with_gyro(90)
    straight_line_test(15)
    turn_with_gyro(90)
    straight_line_test(15)
    turn_with_gyro(90)
    straight_line_test(15)
    turn_with_gyro(90)

def turn_with_gyro(target_angle, speed=15):
    gyro.reset()
    sleep(0.1)
    if target_angle > 0:
        tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))
        while gyro.angle < target_angle:
            sleep(0.01)
    else:
        tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))
        while gyro.angle > target_angle:
            sleep(0.01)

    tank_drive.off()
    print("Target angle:", target_angle, "Measured:", gyro.angle, "Error:", target_angle-gyro.angle)


def lemniscate(numTimes):
  gyro.reset
  intial_lpos = left_motor.position
  intial_rpos = right_motor.position
  speed = 25
  length = 194
  rotations = length / wheel_circ
  time = length/speed
  steps = 200
  steps_rot = rotations /steps
  for i in range(numTimes):
    for j in range(0, steps):
      k_prime = math.cos(2*math.pi*(j/steps))
      right_speed = speed*(1+k_prime)
      left_speed = speed*(1-k_prime)
      tank_drive.on_for_rotations(SpeedPercent(left_speed), SpeedPercent(right_speed), steps_rot)
    tank_drive.off()
    print ("Gyro Orientation: ", gyro.angle)
    print ("Left wheel position: ", left_motor.position -intial_lpos)
    print ("Right wheen positon: ", right_motor.position -intial_rpos)

def lemniscate_green_floor(numTimes):
  intial_lpos = left_motor.position
  intial_rpos = right_motor.position
  gyro.reset()
  speed = 12
  speed_cms = map_speed(speed)
  length = 7.5 * 3/2 * axle_length
  time = length / speed
  rotations = length / wheel_circ
  steps = int(100 * time)
  steps_rot = rotations /steps
  time_steps = time/steps
  k_prime_array = []
  for j in range(0, steps):
    k_prime_array.append(math.cos(2*math.pi*(j/steps)))
  for i in range(numTimes):
    for j in range(0, steps):
      right_speed = speed*(1+k_prime_array[j])
      left_speed = speed*(1-k_prime_array[j])
      tank_drive.on(SpeedPercent(left_speed), SpeedPercent(right_speed))
      sleep(time_steps)
    tank_drive.off()
    print ("Gyro Orientation: ", gyro.angle)
    print ("Left wheel position: ", left_motor.position - intial_lpos)
    print ("Right wheen positon: ", right_motor.position - intial_rpos)


while 1:
  print('''
  ------------------------
  Activities:
  rotation_test
  straight_line_test
  drive_straight
  turn
  rectangle
  rectangle_gyro
  lemniscate
  lemniscate_green_floor
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
  elif (activity == "rectangle"):
    rectangle(int(input("Number of Times: ")))
  elif (activity == "rectangle_gyro"):
    rectangle_gyro(int(input("Number of Times: ")))
  elif (activity == "lemniscate"):
    lemniscate(int(input("Number of Times: ")))
  elif (activity == "lemniscate_green_floor"):
    lemniscate_green_floor(int(input("Number of Times: ")))