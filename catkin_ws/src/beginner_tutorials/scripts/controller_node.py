#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies

import rospy
import time


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
AxisRoll        = 0
AxisPitch       = 1
AxisYaw         = 3
AxisZ           = 4

# define the default scaling to apply to the axis inputs. useful where an axis is inverted
ScaleRoll       = 1.0
ScalePitch      = 1.0
ScaleYaw        = 1.0
ScaleZ          = 1.0

DroneState = False
# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	global DroneState
	if (DroneState == False):
		if data.buttons[ButtonEmergency]==1:
			#rospy.loginfo("Emergency Button Pressed")
			print("Emergency")
		elif data.buttons[ButtonLand]==1:
			#rospy.loginfo("Land Button Pressed")
			print("Landing")
		elif data.buttons[ButtonTakeoff]==1:
			#rospy.loginfo("Takeoff Button Pressed")
			print("Takeoff")
	if (data.buttons[ButtonAuto]==1):
		DroneState ^= True
		print("Autonomous, DroneState: ", DroneState)
		
def AutoMessage():
		

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

	# Now we construct our Qt Application and associated controllers and windows
	app = QtGui.QApplication(sys.argv)
	# executes the QT application
	#display.show()
	print("Hello")

	# subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	subJoystick = rospy.Subscriber('/joy', Joy, ReceiveJoystickMessage)
	subAuto = rospy.Subscriber('/auto',auto, 
	print("We get to app.exec()")
	status = app.exec_()
	print("Hello3")
	rospy.signal_shutdown('Great Flying!')
	print("Hello4")
	sys.exit(status)
