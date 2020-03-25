#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
import time
#from testing.msg import IntList
from std_msgs.msg import Int64



# For Topic Correction
DroneID = "FR"

# Global Values

# 0 is axis roll (left and right)
# 1 is axis pitch (forward and backward)
# 2 is axis yaw (rotate left and right)
# 3 is axis z (vertical up and down)
axis = [0,0,0,0]
direction = 1
acelleration = 0.10
id_index = 1

DroneState = True
Autodata = []
init_sweep = False
t_beg = 0
max_result = 400


def phase_2(msg):
	global Autodata
	global init_sweep
	global axis
	global direction
	global id_index
	global max_result
	global acelleration
	#rospy.loginfo("Autodata: %s",Autodata)
	if (init_sweep == 0):
		Autodata.append(msg.data)
		rospy.loginfo("Sweeping Out")
		if (len(Autodata) == 5):
			init_sweep = 1
		axis[id_index] = acelleration*direction
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif (init_sweep == 1):
		max_result = max(Autodata)
		if ( abs(max_result-msg.data) < 100):
			init_sweep = 2
		rospy.loginfo("Sweeping Back")
		axis[id_index] = acelleration*direction*-1
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
	elif (init_sweep == 2):
		axis[id_index] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		init_sweep = 3
		rospy.loginfo("Finished Phase 2: %s",axis)
	else:
		axis[id_index] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		rospy.loginfo("Else State: %s",axis)
		
def phase_3(msg):
	global max_result
	rospy.loginfo("Max :%s, Msg.data: %s",max_result,msg.data)
	if (msg.data > max_result):
		max_result = msg.data
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*1
		rospy.loginfo("Forward: %s",axis)
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif ( msg.data < max_result) :
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*-1
		rospy.loginfo("Reverse: %s",axis)
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif (abs(max_result-msg.data) < 100):
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		rospy.loginfo("Float: %s",axis)

def AutoCallback(msg):
	global Autodata
	global DroneState
	global init_sweep
	global t_beg
	if (DroneState == True):
		rospy.loginfo("Autonomous Recieved: %s", msg.data)
		if (init_sweep==3):
			phase_3(msg)
		else :
			phase_2(msg)
	else :
		rospy.loginfo("Recieved Data!:  %s", msg.data)
		
def listener():
	rospy.Subscriber("data", Int64, AutoCallback)
	rospy.loginfo("Begin communication with Autonomous Node")
	rospy.spin()
	
	
# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('ardrone_joystick_controller')
	# Next load in the parameters from the launch-file
	DroneID 		= str (rospy.get_param("~DroneID",DroneID) )
	
	# Drone ID logic
	rospy.loginfo("ID: %s",DroneID)
	if ( DroneID == 'FL') :
		id_index = 1
		direction = 1
	elif (DroneID == 'FR'):
		id_index = 0
		direction = -1
	elif (DroneID == 'RL'):
		id_index = 0
		direction = 1
	elif (DroneID == 'RR'):
		id_index = 1
		direction =  -1
	else :
		print("Not valid ID!!!!")
		id_index = 1
		direction  = 0
	
	listener()
	
	rospy.signal_shutdown('Great Flying!')
	sys.exit()
