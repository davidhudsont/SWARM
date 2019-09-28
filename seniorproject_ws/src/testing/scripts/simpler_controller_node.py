#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies

import rospy
from time import sleep
from testing.msg import IntList
from std_msgs.msg import Int64
# Import the joystick message
from sensor_msgs.msg import Joy

# Finally the GUI libraries
from PySide import QtCore, QtGui

# define the default mapping between joystick buttons and their corresponding actions
ButtonEmergency = 0
ButtonLand      = 1
ButtonTakeoff   = 2
ButtonAuto = 3
ButtonThrsh = 4
ButtonHighCon = 5
# define the default mapping between joystick axes and their corresponding directions
AxisRoll        = 1
AxisPitch       = 0
AxisYaw         = 2
AxisZ           = 5

# define the default scaling to apply to the axis inputs. useful where an axis is inverted
ScaleRoll       = 1.0
ScalePitch      = 1.0
ScaleYaw        = 1.0
ScaleZ          = 1.0

Group = ""
DroneID = "FR"

DroneState = False
thresh_state = False
highcon_state = False
Autodata = []
phase = 0
max_result = 400
threshold = 1500
# 0 is speed roll (left and right)
# 1 is speed pitch (forward and backward)
# 2 is speed yaw (rotate left and right)
# 3 is speed z (vertical up and down)
axis = [0,0,0,0]
direction = 1
acelleration = 0.10
id_index = 1

# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	global DroneState
	global Autodata
	global thresh_state
	global highcon_state
	global phase
	rospy.loginfo("THR: %s, HGH: %s",thresh_state,highcon_state)
	if (DroneState == False):
		Autodata = []
		phase = 0
		if data.buttons[ButtonThrsh]==1:
			if (highcon_state == False and thresh_state == False):
				thresh_state = True
			else:
				thresh_state^= thresh_state
		elif data.buttons[ButtonHighCon]==1:
			if (thresh_state ==False and highcon_state == False):
				highcon_state = True
			else:
				highcon_state^= highcon_state
		elif data.buttons[ButtonEmergency]==1:
			#rospy.loginfo("Emergency Button Pressed")
			print("Emergency")
		elif data.buttons[ButtonLand]==1:
			#rospy.loginfo("Land Button Pressed")
			print("Landing")
		elif data.buttons[ButtonTakeoff]==1:
			#rospy.loginfo("Takeoff Button Pressed")
			print("Takeoff")
			
		else : 
			#controller.SetCommand(data.axes[AxisRoll]/ScaleRoll,data.axes[AxisPitch]/ScalePitch,data.axes[AxisYaw]/ScaleYaw,data.axes[AxisZ]/ScaleZ)
			print(data.axes)
			print(data.buttons)
	if (data.buttons[ButtonAuto]==1):
		DroneState ^= True

def find_high_concentration(msg):
	global Autodata
	global phase
	global axis
	global direction
	global id_index
	global max_result
	global acelleration
	#rospy.loginfo("Autodata: %s",Autodata)
	if (phase == 0):
		Autodata.append(msg.data)
		rospy.loginfo("Sweeping Out")
		if (len(Autodata) == 5):
			phase = 1
		axis[id_index] = acelleration*direction
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif (phase == 1):
		max_result = max(Autodata)
		if ( abs(max_result-msg.data) < 100):
			phase = 2
		rospy.loginfo("Sweeping Back")
		axis[id_index] = acelleration*direction*-1
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
	elif (phase == 2):
		rospy.loginfo("Finished Phase 2")
		axis[id_index] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		phase = 3
	else:
		axis[id_index] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		rospy.loginfo("Else State")
		
def follow_highest_concentration(msg):
	global Autodata
	global max_result
	if (msg.data > max_result):
		max_result = msg.data
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*1
		rospy.loginfo("Forward")
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif ( msg.data < max_result) :
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*-1
		rospy.loginfo("Reverse")
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif (abs(max_result-msg.data) < 100):
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*0
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		rospy.loginfo("Float")

def threshold_find(msg):
	global Autodata
	global phase
	global axis
	global direction
	global id_index
	global max_result
	global acelleration
	global delay
	global threshold
	#rospy.loginfo("Autodata: %s",Autodata)
	if (phase == 0):
		Autodata.append(msg.data)
		rospy.loginfo("Sweeping Out")
		if (abs(msg.data-threshold) <= 500):
			rospy.loginfo("Found Threshold")
			axis[id_index] = acelleration*direction*0
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
			delay = 5-len(Autodata) 
			phase = 1
		elif (len(Autodata) == 5):
			phase = 1
			axis[id_index] = acelleration*direction*0
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		axis[id_index] = acelleration*direction
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	

def threshold_track(msg):
	global Autodata
	global threshold
	global acelleration
	global direction
	if (msg.data > max_result):
		max_result = msg.data
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*1
		rospy.loginfo("Forward")
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif ( msg.data < max_result) :
		axis = [0,0,0,0]
		axis[1] = acelleration*direction*-1
		rospy.loginfo("Reverse")
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
	elif (abs(threshold-msg.data) < 500):
		axis = [0,0,0,0]
		acelleration = 0.1
		axis[1] = acelleration*direction
		#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		ropsy.loginfo("Float")
	
def AutoCallback(msg):
	global Autodata
	global DroneState
	global phase
	global t_beg
	global controller
	global delay
	#~ rospy.loginfo("Battery : %s, VX: %s, VY: %s, VZ: %s, Altitude: %s",controller.bat,controller.vx,controller.vy,controller.vz,controller.altitude)
	if (DroneState == True):
		rospy.loginfo("Autonomous %s, Phase: %s", msg.data,phase)
		if (thresh_state == True):
			if (phase==2):
				sleep(delay)
				threshold_track(msg)
			else :
				threshold_find(msg)
		elif (highcon_state == True):
			if (phase==3):
				follow_highest_concentration(msg)
			else :
				find_high_concentration(msg)		
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
	ButtonEmergency = int (   rospy.get_param("~ButtonEmergency",ButtonEmergency) )
	ButtonLand      = int (   rospy.get_param("~ButtonLand",ButtonLand) )
	ButtonTakeoff   = int (   rospy.get_param("~ButtonTakeoff",ButtonTakeoff) )
	ButtonAuto		= int (	  rospy.get_param("~ButtonAuto",ButtonAuto) )
	ButtonThrsh		= int (   rospy.get_param("~ButtonThrsh",ButtonThrsh) )
	ButtonHighCon 	= int (	  rospy.get_param("~ButtonHighCon",ButtonHighCon) )
	AxisRoll        = int (   rospy.get_param("~AxisRoll",AxisRoll) )
	AxisPitch       = int (   rospy.get_param("~AxisPitch",AxisPitch) )
	AxisYaw         = int (   rospy.get_param("~AxisYaw",AxisYaw) )
	AxisZ           = int (   rospy.get_param("~AxisZ",AxisZ) )
	ScaleRoll       = float ( rospy.get_param("~ScaleRoll",ScaleRoll) )
	ScalePitch      = float ( rospy.get_param("~ScalePitch",ScalePitch) )
	ScaleYaw        = float ( rospy.get_param("~ScaleYaw",ScaleYaw) )
	ScaleZ          = float ( rospy.get_param("~ScaleZ",ScaleZ) )
	Group 			= str	( rospy.get_param("~Group",Group) )
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
	# Now we construct our Qt Application and associated controllers and windows
	#app = QtGui.QApplication(sys.argv)
	# executes the QT application
	#display.show()
	# subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	topic_name = Group+"/joy"
	subJoystick = rospy.Subscriber(topic_name, Joy, ReceiveJoystickMessage)
	print("subJoystick",subJoystick)
	listener()
	#~ while(True):
		#~ i = 1
	#status = app.exec_()
	rospy.signal_shutdown('Great Flying!')
	sys.exit()
