#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies

import rospy
import time
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
DroneID = "FR"

DroneState = False
Autodata = []
init_sweep = False
t_beg = 0


# 0 is speed roll (left and right)
# 1 is speed pitch (forward and backward)
# 2 is speed yaw (rotate left and right)
# 3 is speed z (vertical up and down)
axis = [0,0,0,0]
direction = 1
acelleration = 0.10
id_index = 1

DroneState = False
Autodata = []
init_sweep = False
t_beg = 0
max_result = 400

# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	global DroneState
	global init_sweep
	global Autodata
	if (DroneState == False):
		Autodata = []
		init_sweep = 0
		if data.buttons[ButtonEmergency]==1:
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
			print("Axes ",data.axes)
			print("ID: ",DroneID)
	if (data.buttons[ButtonAuto]==1):
		DroneState ^= True
		
def listener():
	rospy.Subscriber("data", Int64, AutoCallback)
	rospy.spin()		


	
def phase_0(data):
	global Autodata
	if (len(Autodata) <= 5):
		Autodata.append(data.data)
		#controller.SetCommand(0.0/ScaleRoll,0.25/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)	
	else:
		#controller.SetCommand(0/ScaleRoll,0.0/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
		print(Autodata)
		
def phase_1(data):
	global Autodata
	global init_sweep
	rospy.loginfo("Autodata: %s",Autodata)
	if (init_sweep == 0):
		Autodata.append(data.data)
		rospy.loginfo("Sweeping Out")
		if (len(Autodata) == 5):
			init_sweep = 1
		#controller.SetCommand(0.0/ScaleRoll,0.25/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)	
	elif (init_sweep == 1):
		tmp = max(Autodata)
		if ( abs(tmp-data.data) < 30):
			init_sweep = 2
		rospy.loginfo("Sweeping Back")
		#controller.SetCommand(0.0/ScaleRoll,-0.25/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
	elif (init_sweep == 2):
		rospy.loginfo("Drone Stop")
		#controller.SetCommand(0/ScaleRoll,0.0/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
	else:
		#controller.SetCommand(0/ScaleRoll,0.0/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
		ropsy.loginfo("Else")

def phase_2(data):
	global Autodata
	global init_sweep
	global axis
	global direction
	global id_index
	global max_result
	global acelleration
	rospy.loginfo("Autodata: %s",Autodata)
	if (init_sweep == 0):
		Autodata.append(data.data)
		rospy.loginfo("Sweeping Out")
		if (len(Autodata) == 5):
			init_sweep = 1
		axis[id_index] = acelleration*direction
		rospy.loginfo("Axis: %s",axis)
		#print("axis: ",axis)
		#controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		time.sleep(.250)
	elif (init_sweep == 1):
		max_result = max(Autodata)
		if ( abs(max_result-data.data) < 30):
			init_sweep = 2
		rospy.loginfo("Sweeping Back")
		axis[id_index] = acelleration*direction*-1
		rospy.loginfo("Axis: %s",axis)
		#controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
	elif (init_sweep == 2):
		rospy.loginfo("Drone Stop")
		axis[id_index] = acelleration*direction*0
		rospy.loginfo("Axis: %s",axis)
		#controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		init_sweep = 3
	else:
		axis[id_index] = acelleration*direction*0
		rospy.loginfo("Axis: %s",axis)
		#controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		rospy.loginfo("Else")
		
	

def AutoCallback(data):
	global Autodata
	global DroneState
	global init_sweep
	global t_beg
	if (DroneState == True):
		rospy.loginfo("Autonomous %s", data.data)
		phase_2(data)
	else :
		rospy.loginfo("I see data is %s", data.data)
		

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
	AxisRoll        = int (   rospy.get_param("~AxisRoll",AxisRoll) )
	AxisPitch       = int (   rospy.get_param("~AxisPitch",AxisPitch) )
	AxisYaw         = int (   rospy.get_param("~AxisYaw",AxisYaw) )
	AxisZ           = int (   rospy.get_param("~AxisZ",AxisZ) )
	ScaleRoll       = float ( rospy.get_param("~ScaleRoll",ScaleRoll) )
	ScalePitch      = float ( rospy.get_param("~ScalePitch",ScalePitch) )
	ScaleYaw        = float ( rospy.get_param("~ScaleYaw",ScaleYaw) )
	ScaleZ          = float ( rospy.get_param("~ScaleZ",ScaleZ) )
	DroneID 		= str (rospy.get_param("~DroneID",DroneID) )
	print("ID: ",DroneID)
	if ( DroneID == 'FR') :
		id_index = 1
		scale = 1
	elif (DroneID == 'FL'):
		id_index = 0
		scale = -1
	elif (DroneID == 'RR'):
		id_index = 0
		scale = 1
	elif (DroneID == 'RL'):
		id_index = 1
		scale =  -1
	else :
		print("Not valid ID!!!!")
		id_index = 1
		scale  = 0
	# Now we construct our Qt Application and associated controllers and windows
	#app = QtGui.QApplication(sys.argv)
	# executes the QT application
	#display.show()
	# subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	subJoystick = rospy.Subscriber('/joy', Joy, ReceiveJoystickMessage)
	print("subJoystick",subJoystick)
	listener()
	while(True):
		i = 1
	#status = app.exec_()
	rospy.signal_shutdown('Great Flying!')
	sys.exit(status)
