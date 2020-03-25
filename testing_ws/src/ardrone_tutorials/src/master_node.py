#!/usr/bin/env python
import rospy
import time
import random
#from std_msgs.msg import Int64
from std_msgs.msg import Int64
from std_msgs.msg import String

import json

from sensors import drone

drones = []
active_drones = 0

node_count = 0
count = 0
tags = ["FL","FR","RL","RR"]

max_result = 400
threshold = 1500
master_phase = 1

FL = False
FR = False
RL = False
RR = False

def sync_phase(phase):
	global drones
	global active_drones
	count = 0
	for n in drones:
		if (n.phase==phase):
			count +=1
	if (count == active_drones):
		return True
	else:
		return False


def log_data():
		global drones
		for n in drones:
			data = str(n.tag)+"-- rotZ: "+str(n.rotZ)
			data = data+" bat: "+str(n.bat)+" CO2: "+str(n.co2)
			data = data+" Phase: "+str(n.phase)+" Altitude: "+str(n.altitude)
			data = data+" Autodata: "+str(n.Autodata)
			rospy.loginfo(data)

def run():
	global drones
	for n in drones:
		if (n.auto_state==True):
			if (n.phase== 0):
				n.rotate_to_angle(95)
			elif (n.phase == 1):
				n.threshold_find()
			elif(sync_phase()==True):
				n.threshold_track()
		else:
			n.reset_auto()

def  sweep(count):
	global drones
	for n in drones:
		if (n.auto_state==True):
			if (n.phase==0):
				rospy.loginfo("Sweep Out")
				n.threshold_find()
			log_data()
			rate = rospy.Rate(1)
		else:
			n.reset_auto()
			log_data()
			rate = rospy.Rate(1)
	rate.sleep()

def run2(count):
	global drones
	# print(count)
	for n in drones:
		if (n.auto_state==True):
			if (n.phase== 0):
				if (count==3):
					rospy.loginfo("Rotation to Angle: %s",108)
					log_data()
				rate = rospy.Rate(4)
				n.rotate_to_angle_variable(108)
			elif (sync_phase(1)==True):
				log_data()
				n.threshold_find()
				rate = rospy.Rate(1)
			elif(sync_phase(2)==True):
				log_data()
				n.threshold_track()
				rate = rospy.Rate(1)
			else:
				log_data()
				rate = rospy.Rate(1)
		else:
			log_data()
			rate = rospy.Rate(1)
			n.reset_auto()
	rate.sleep()

def drone_rotation_align():
	global drones
	rate = rospy.Rate(4)
	for n in drones:
		n.rotate_to_angle_variable(185)
	rate.sleep()

def climb_altitude(count):
	global drones
	for n in drones:
		if (n.auto_state==True):
			if (n.phase==0):
				if (count==3):
					rospy.loginfo("flying to correct altitude")
					log_data()
				rate = rospy.Rate(4)
				n.raise_to_altitude(1100,2800)
			elif (n.phase == 1):
				rospy.loginfo("Reached correct Altitude")
				rate = rospy.Rate(1)
				log_data()
			else:
				log_data()
				rate = rospy.Rate(1)
		else :
			n.reset_auto()
			rate = rospy.Rate(1)
			log_data()
	rate.sleep()

def add_drones(FL,FR,RL,RR):
	global drones
	global active_drones
	if (FL==True):
		tmp = drone("ardrone1","FL")
		drones.append(tmp)
		active_drones += 1
	if (FR==True):
		tmp = drone("ardrone2","FR")
		drones.append(tmp)
		active_drones += 1
	if (RL==True):
		tmp = drone("ardrone3","RL")
		drones.append(tmp)
		active_drones += 1
	if (RR==True):
		tmp = drone("ardrone4","RR")
		drones.append(tmp)
		active_drones += 1
	

def run3(count):
	global drones
	for n in drones:
		if (n.auto_state==True):
			if (n.phase==0):
				if (count==3):
					rospy.loginfo("Flying to correct altitude")
					log_data()
				rate = rospy.Rate(4)
				n.raise_to_altitude(3000,4700)
			elif (n.phase==1):
				if (count==3):
					rospy.loginfo("Rotating to correct")
					log_data()
				n.rotate_to_angle_variable(0)
				rate = rospy.Rate(4)
			elif (n.phase==2):
				rospy.loginfo("Sweep out")
				log_data()
				n.threshold_find()
				rate = rospy.Rate(1)
			elif (n.phase==3):
				rospy.loginfo("Tracking")
				log_data()
				n.threshold_track()
				rate = rospy.Rate(1)
			else:
				log_data()
				rate = rospy.Rate(1)
		else:
			n.reset_auto()
			log_data()
			rate = rospy.Rate(1)
	rate.sleep()


def run4(count):
	global drones
	global master_phase
	if (sync_phase(master_phase)):
		master_phase += 1
	for n in drones:
		if (n.auto_state==True):
			if (n.phase==0):
				if (count==3):
					rospy.loginfo("Flying to correct altitude")
					log_data()
				rate = rospy.Rate(4)
				n.raise_to_altitude(2500,4700)
			elif (master_phase==1):
				if (count==3):
					rospy.loginfo("Rotating to correct")
					log_data()
				n.rotate_to_angle_variable(78)
				rate = rospy.Rate(4)
			elif (master_phase==2):
				rospy.loginfo("Sweep out")
				log_data()
				n.threshold_find()
				rate = rospy.Rate(1)
			elif (n.phase==3):
				rospy.loginfo("Tracking")
				log_data()
				n.threshold_track()
				rate = rospy.Rate(1)
			else:
				log_data()
				rate = rospy.Rate(1)
		else:
			n.reset_auto()
			log_data()
			rate = rospy.Rate(1)
	rate.sleep()



if __name__ == '__main__':
	rospy.init_node('master', anonymous=True)
	rospy.loginfo("MASTER NODE INITIALIZED")
	FL = bool (rospy.get_param("~FL", FL) )
	FR = bool (rospy.get_param("~FR", FR) )
	RL = bool (rospy.get_param("~RL", RL) )
	RR = bool (rospy.get_param("~RR", RR) ) 

	add_drones(FL,FR,RL,RR)
	# rate = rospy.Rate(4)
	count = 0
	while not rospy.is_shutdown():
		if (count==4):
			count = 0

		# run_drones()
		# drone_rotation_align()
		# run2(count)
		# climb_altitude(count)
		# run3(count)
		# sweep(count)
		run3(count)
		count += 1
		# rate.sleep()
