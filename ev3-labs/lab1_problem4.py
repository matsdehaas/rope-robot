"""
Group Members: Aemad Qamar

Date: 18/09/2025
 
Brick Number: 3

Lab Number: 1

Problem Number: 4
 
Brief Program/Problem Description: 

	Create an algorithm that can return the position of a robot in an xy coordinate
  system, based on a series of inputs for both motors.

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

def map_speed(speed):
  if 0.4778*speed <= 34:
    return 0.4778*speed
  else:
    return 34

def normalize_orientation(orientation):
  while (orientation < 0):
    orientation += 2*math.pi
  while (orientation > 2*math.pi):
    orientation -= 2*math.pi
  return(orientation)

def calculateTranslation(curr_theta, curr_x, curr_y, lSpeed, RSpeed, time, steps_per_second):
  w = (map_speed(lSpeed)- map_speed(RSpeed))/ (axle_length)
  steps = steps_per_second*time
  step_width = 1/steps_per_second
  avg_speed = (map_speed(RSpeed) + map_speed(lSpeed)) /2

  for i in range(1, steps+1): ## right hand rectangle approximation
    curr_theta += w *step_width
    curr_x+= step_width * avg_speed * math.cos(curr_theta)
    curr_y += step_width * avg_speed * math.sin(curr_theta)
  curr_theta = normalize_orientation(curr_theta)
  return curr_theta, curr_x, curr_y

def dead_reckoning(array): # 80 60 2 60 60 1 -50 80 2
  l1 = int(array.split()[0])
  r1 = int(array.split()[1])
  s1 = int(array.split()[2])
  l2 = int(array.split()[3])
  r2 = int(array.split()[4])
  s2 = int(array.split()[5])
  l3 = int(array.split()[6])
  r3 = int(array.split()[7])
  s3 = int(array.split()[8])
  x = 0 ## cm
  y = 0 ## cm
  orientation = 0 ## radians
  initial_Lpos= left_motor.position
  initial_Rpos = right_motor.position
  steps_per_second = 1000

  gyro.reset()

  orientation,x,y = calculateTranslation(orientation,x,y,l1,r1,s1,steps_per_second)
  print("Expected orientation, x, and y: ", orientation*180/math.pi, x, y)
  orientation,x,y = calculateTranslation(orientation,x,y,l2,r2,s2,steps_per_second)
  print("Expected orientation, x, and y: ", orientation*180/math.pi, x, y)
  orientation,x,y = calculateTranslation(orientation,x,y,l3,r3,s3,steps_per_second)
  print("Expected orientation, x, and y: ", orientation*180/math.pi, x, y)

  tank_drive.on(SpeedPercent(l1), SpeedPercent(r1))
  sleep(s1)
  print("Gyro orientation: ", gyro.angle)
  print ("Left wheel position: ", left_motor.position - initial_Lpos)
  print ("Right wheen positon: ", right_motor.position - initial_Rpos)
  print("Position of Robot: ", (left_motor.position +right_motor.position)/2)

  tank_drive.on(SpeedPercent(l2), SpeedPercent(r2))
  sleep(s2)
  print("Gyro orientation: ", gyro.angle)
  print ("Left wheel position: ", left_motor.position - initial_Lpos)
  print ("Right wheen positon: ", right_motor.position - initial_Rpos)
  print("Position of Robot: ", (left_motor.position +right_motor.position)/2)

  tank_drive.on(SpeedPercent(l3), SpeedPercent(r3))
  sleep(s3)
  print("Gyro orientation: ", gyro.angle)
  print ("Left wheel position: ", left_motor.position - initial_Lpos)
  print ("Right wheen positon: ", right_motor.position - initial_Rpos)
  print("Position of Robot: ", (left_motor.position +right_motor.position)/2)
  tank_drive.off()

def test_distance(speed):
  tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))
  sleep(1)
  tank_drive.off()

while 1:
  print('''
  ------------------------
  Activities:
  dead_reckoning
  test_distance
  ------------------------
  ''')
  activity = input("Enter activity: ")
  if (activity == "dead_reckoning"):
    dead_reckoning(input("Insert the 3x3 array (ssv): "))
  elif (activity == "test_distance"):
    test_distance(int(input("Enter Speed: ")))
  