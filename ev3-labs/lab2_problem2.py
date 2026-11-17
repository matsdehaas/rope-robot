"""
Group Members: Mats de Haas, Aemad Qamar

Date: 04/10/2025

Brick Number: 3

Lab Number: 2

Problem Number: 2

Brief Program/Problem Description: 

	Forward kinematics
	b) Given two angles, the robot moves to their corresponding joint angles, 
    and returns the (x,y) position of the end effector.
    c)	i. Manually move the end effector to two different points and return the 
		distance between them.
        ii. Manually move the end effector to three different points where p1 and p2
        are respectively on line 1 and line 2, and p0 is on the intersection between
        the lines. Return the angle of the two lines.
    
    

Brief Solution Summary:

  	The method calc_forward_kinematics translates two theta values to a x,y coordinate
    by using the forward kinematic formula for a 2-DOF robot arm. 
    For problem 2b the angles of the motors are set to t1 and t2 and calc_forward_kinematics
    is called to calculate the position of the end effector.
    
    For measuring distance, the t1 and t2 of both points are recorded and sent to 
    the calc_forward_kinematics method to find the coordinates of both points. 
    After this, the Euclidean distance is calculated and returned.
    
    For measuring the angle, the same process for recording and calculating the 
    coordinates is used. After this, the two lines are converted to vectors. Then
    finally the angle between these two vectors can be calculated using the corresponding
    formula.

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
#!/usr/bin/env python3
from time import sleep
import math as m
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import TouchSensor
l1 = 11.3 #cm
l2 = 5 #cm
speed = 15
ts = TouchSensor()

m1 = LargeMotor(OUTPUT_A)
m2 = LargeMotor(OUTPUT_B)

def radians(t1, t2):
    t1 = t1 /180 * m.pi
    t2 = t2 /180 * m.pi
    return t1, t2


def calc_forward_kinematics(t1, t2):
    t1, t2 = radians(t1, t2)
    x = l1 * m.cos(t1) + l2 * m.cos(t1+t2)
    y = l1 * m.sin(t1) + l2 * m.sin(t1+t2)
    return x,y

def move_forward_kinematics(t1, t2):
    m1.on_for_degrees(speed, t1)
    m2.on_for_degrees(speed, t2)
    m1.off()
    m2.off()

def move_to_point():
    t1,t2 = input("Enter t1 and t2: ").split()
    t1 = int(t1)
    t2 = int(t2)
    print("intial pos:", -m1.position, m2.position)
    x,y = calc_forward_kinematics(t1, t2)
    move_forward_kinematics(-t1,t2)
    print("final pos:", -m1.position, m2.position)
    print("x:",format_number(x),"y:",format_number(y))
    input("return?")
    move_forward_kinematics(-m1.position,-m2.position)

x = 9.98087141305093e-16
y = 16.3

def format_number(num):
    if abs(num) < 0.01:
        return "0"
    else:
        s = "%.2f" % num
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

def measure_distance():
    pointList = []
    count = 0
    while count != 2:
        if ts.is_pressed:
            print(-m1.position,m2.position)
            pointList.extend(calc_forward_kinematics(-m1.position,m2.position))
            count += 1
            sleep(1)
    dx = pointList[0] - pointList[2]
    dy = pointList[1] - pointList[3]
    print("Distance:",m.sqrt(dx ** 2 + dy ** 2))

def measure_angle():
    pointList = []
    count = 0
    while count != 3:
        if ts.is_pressed:
            print(-m1.position,m2.position)
            print(calc_forward_kinematics(-m1.position,m2.position))
            pointList.extend(calc_forward_kinematics(-m1.position,m2.position))
            count += 1
            sleep(1)

    # direction vectors starting from p0.   0 1  2 3  4 5
    v1 = (pointList[2] - pointList[0], pointList[3] - pointList[1])
    v2 = (pointList[4] - pointList[0], pointList[5] - pointList[1])

    # dot product and cross product
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    cross = v1[0]*v2[1] - v1[1]*v2[0]

    # angle in radians, then convert to degrees
    theta = m.atan2(abs(cross), dot)
    return m.degrees(theta)

while 1:
    print("""
          _________________________
          Activities:
          move_to_point
          measure_distance
          measure_angle
          _________________________
          """)
    activity = input("Choose activity: ")
    if (activity == "move_to_point"):
        m1.position=0
        m2.position=0
        move_to_point()
        m1.off(brake=False)
        m2.off(brake=False)
    elif (activity == "measure_distance"):
        m1.position=0
        m2.position=0
        measure_distance()
    elif (activity == "measure_angle"):
        m1.position=0
        m2.position=0
        print(measure_angle())
