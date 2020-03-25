#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64
from sensors import drone
from sensors import gps
from sensors import imu
from PID_Controller import PID
from time import sleep

drones = []

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def map(x, in_min, in_max, out_min, out_max) :
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def drone_rotation_align(angle):
	global drones
	for n in drones:
		n.rotate_to_angle(angle)
	
def add_drones(FL,FR,RL,RR):
	global drones
	if (FL==True):
		d0 = drone("ardrone1","FL")
		print(d0)
		drones.append(d0)
	if (FR==True):
		d1 = drone("ardrone1","FR")
		print(d1)
		drones.append(d1)
	if (RL==True):
		d2 = drone("ardrone3","RL")
		drones.append(d2)
		print(d2)
	if (RR==True):
		d3 = drone("ardrone4","RR")
		drones.append(d3)
		print(d3)

def run_drones():
	global drones
	for n in drones:
		n.run()

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

if __name__ == '__main__':

	# add_drones(True,False,True,False)
	# print(drones)
	
	# x = input("Input Start: ")
	# y = input("Input End: ")
	# i0 = imu(x)
	# i0.pid_move_to_angle(y)
	for x in my_range(700,2400,100):
		y = map(x,2500,700,0.1,1.0)
		print(x,y)

	x = 3500
	y = map(x,2500,2800,-0.1,-1.0)
	print(x,y)

	# while (True):
	# 	for n in my_range(0,180,10):
	# 		pid = p.update(n)
	# 		scaled = map(pid,2396.0,188.0,0,1.0)
	# 		print(n,pid,scaled)
	# 		sleep(1)