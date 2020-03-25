#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
from time import sleep
#from testing.msg import IntList
from std_msgs.msg import Int64
from std_msgs.msg import String
# Import the joystick message
from sensor_msgs.msg import Joy

# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay

# Finally the GUI libraries
from PySide import QtCore, QtGui

import json

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
AxisUD			= 7
AxisLR 			= 6

# define the default scaling to apply to the axis inputs. useful where an axis is inverted
ScaleRoll       = 1.0
ScalePitch      = 1.0
ScaleYaw        = 1.0
ScaleZ          = 1.0


DroneID = "FR"


DroneState = False
DisableState = False
angle = 90

# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	global DroneState
	global angle
	global DroneID
	global DisableState
	if (DroneState == False and DisableState == False):
		if data.buttons[ButtonEmergency]==1:
			rospy.loginfo("Emergency Button Pressed")
			controller.SendEmergency()
		elif data.buttons[ButtonLand]==1:
			rospy.loginfo("Land Button Pressed")
			controller.SendLand()
		elif data.buttons[ButtonTakeoff]==1:
			rospy.loginfo("Takeoff Button Pressed")
			controller.SendTakeoff()
		else : 
			controller.SetCommand(data.axes[AxisRoll]/ScaleRoll,data.axes[AxisPitch]/ScalePitch,data.axes[AxisYaw]/ScaleYaw,data.axes[AxisZ]/ScaleZ)
			#~ rospy.loginfo("Axes %s",data.axes)
			#~ rospy.loginfo("VX: %s, VY: %s, VZ: %s, Altitude: %s",controller.velx,controller.vely,controller.velz,controller.altitude)
	if (DisableState == False):
		if (data.buttons[ButtonAuto]==1):
			DroneState ^= True
			if (DroneState == True):
				rospy.loginfo("Entering Autonomous")
			else :
				rospy.loginfo("Exiting Autonomous")
	if (data.axes[AxisUD]==1 and DroneID == "FR" ):
		rospy.loginfo("FR Enable/Disable: %s",DisableState)
		DisableState ^= True
	elif (data.axes[AxisUD]==-1 and DroneID == "RR"):
		rospy.loginfo("RR Enable/Disable: %s",DisableState)
		DisableState ^= True
	elif (data.axes[AxisLR]==1 and DroneID == "FL" ):
		rospy.loginfo("FL Enable/Disable: %s",DisableState)
		DisableState ^= True
	elif ( data.axes[AxisLR]==-1 and DroneID == "RL" ):
		rospy.loginfo("RL Enable/Disable: %s",DisableState)
		DisableState ^= True


def Publish_Commands():
	global controller
	global DroneState
	global DroneID
	global angle
	pub = rospy.Publisher("ardrone/controller", String, queue_size=10)
	rate = rospy.Rate(4)
	while not rospy.is_shutdown():
		msg = String()
		if (controller.rotZ < 0):
			rotZ = 360.0 + controller.rotZ
		else :
			rotZ = controller.rotZ
		if (controller.wa < 0):
			wa = 360.0 + controller.wa
		else :
			wa = controller.wa
		# js = {"ID":DroneID,"state":DroneState,"ws":controller.ws,"wa":wa,"rotZ":rotZ, "bat":controller.bat, "angle":angle}		
		js = {"tag":DroneID,"state":DroneState,"ws":controller.ws,"wa":wa,"rotZ":rotZ, "bat":controller.bat,"alt":controller.altitude}
		msg = json.dumps(js)
		# rospy.loginfo("Sent: %s",msg)
		pub.publish(msg)
		rate.sleep()

def AutoCallback(msg):
	js = json.loads(msg.data)
	global DroneState
	if (DroneState == True):
		# rospy.loginfo("Autonomous %s", msg.data)
		axis = js["axis"]
		# rospy.loginfo("Axis!:  %s",axis)
		controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		
def listener():
	sub = rospy.Subscriber("ardrone/commands", String, AutoCallback)
	
	
	
	
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
	AxisUD			= int (	  rospy.get_param("~AxisUD",AxisUD ) ) 
	AxisLR			= int (	  rospy.get_param("~AxisLR",AxisLR) )
	ScaleRoll       = float ( rospy.get_param("~ScaleRoll",ScaleRoll) )
	ScalePitch      = float ( rospy.get_param("~ScalePitch",ScalePitch) )
	ScaleYaw        = float ( rospy.get_param("~ScaleYaw",ScaleYaw) )
	ScaleZ          = float ( rospy.get_param("~ScaleZ",ScaleZ) )
	DroneID 		= str (rospy.get_param("~DroneID",DroneID) )
	
	
	#~ app = QtGui.QApplication(sys.argv)										# construct video gui
	#display = DroneVideoDisplay(Group)											# start video display
	controller = BasicDroneController() 									# construct Drone Controller
	topic_name = "joy"												# set topic name for joystick
	subJoystick = rospy.Subscriber(topic_name, Joy, ReceiveJoystickMessage) # subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	
	#display.show()
	listener()
	Publish_Commands()
	#~ status = app.exec_()
	#~ while (True):
		#~ sleep(1)
	
	rospy.signal_shutdown('Great Flying!')
	#~ sys.exit(status)
	sys.exit()
	
