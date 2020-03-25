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
# Import the joystick message
from sensor_msgs.msg import Joy

# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay

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

# For Topic Correction
Group = ""
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

DroneState = False
Autodata = []
phase = 0
max_result = 400
threshold = 1500
# handles the reception of joystick packets

class JoystickDroneController(object):
	def __init__(self,name=""):
		rospy.init_node('ardrone_joystick_controller')
		# Next load in the parameters from the launch-file
		ButtonEmergency = int (   rospy.get_param("~ButtonEmergency",ButtonEmergency) )
		ButtonLand      = int (   rospy.get_param("~ButtonLand",ButtonLand) )
		ButtonTakeoff   = int (   rospy.get_param("~ButtonTakeoff",ButtonTakeoff) )
		ButtonAutoReset	= int (	  rospy.get_param("~ButtonAutoReset",ButtonAutoReset) )
		ButtonThresh 	= int (   rospy.get_param("~ButtonThresh", ButtonThresh) )
		ButtonHighConcen= int (   rospy.get_param("~ButtonHighConcen", ButtonHighConcen) )
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
		#app = QtGui.QApplication(sys.argv)										# construct video gui
		#display = DroneVideoDisplay(Group)											# start video display
		controller = BasicDroneController(name) 									# construct Drone Controller
		subJoystick = rospy.Subscriber(topic_name+"/joy", Joy, ReceiveJoystickMessage) # subscribe to the /joy topic and handle messages of type Joy with the function 
		sensor = rospy.Subscriber("data", Int64, AutoCallback)
	def ReceiveJoystickMessage(data):
		global DroneState
		global phase
		global Autodata
		if (DroneState == False):
			Autodata = []
			phase = 0
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
				#rospy.loginfo("Axes %s",data.axes)
				rospy.loginfo("VX: %s, VY: %s, VZ: %s, Altitude: %s",controller.velx,controller.vely,controller.velz,controller.altitude)
		if (data.buttons[ButtonAuto]==1):
			DroneState ^= True
			if (DroneState == True):
				rospy.loginfo("Entering Autonomous")
			else :
				rospy.loginfo("Exiting Autonomous")	

	def RecieveSensorMessage(msg):
		global Autodata
		global DroneState
		global phase
		global t_beg
		global controller
		rospy.loginfo("Battery : %s, VX: %s, VY: %s, VZ: %s, Altitude: %s",controller.bat,controller.vx,controller.vy,controller.vz,controller.altitude)
		if (DroneState == True):
			rospy.loginfo("Autonomous %s", msg.data)
			if (phase==3):
				phase_3(data)
			phase_2(data)
		else :
			rospy.loginfo("Recieved Data!:  %s", msg.data)

	def DroneLogic():
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
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		elif (phase == 1):
			max_result = max(Autodata)
			if ( abs(max_result-msg.data) < 100):
				phase = 2
			rospy.loginfo("Sweeping Back")
			axis[id_index] = acelleration*direction*-1
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		elif (phase == 2):
			rospy.loginfo("Finished Phase 2")
			axis[id_index] = acelleration*direction*0
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
			phase = 3
		else:
			axis[id_index] = acelleration*direction*0
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
			rospy.loginfo("Else State")
			
	def follow_highest_concentration(msg):
		global Autodata
		global max_result
		if (msg.data > max_result):
			max_result = msg.data
			axis = [0,0,0,0]
			axis[1] = acelleration*direction*1
			ropsy.loginfo("Forward")
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		elif ( msg.data < max_result) :
			axis = [0,0,0,0]
			axis[1] = acelleration*direction*-1
			ropsy.loginfo("Reverse")
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		elif (abs(max_result-msg.data) < 100):
			axis = [0,0,0,0]
			axis[1] = acelleration*direction*0
			controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
			ropsy.loginfo("Float")

	
# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	
	
	# Drone ID logic
	rospy.loginfo("ID: %s",DroneID)
	
	
	
	
	rospy.signal_shutdown('Great Flying!')
	sys.exit(status)
