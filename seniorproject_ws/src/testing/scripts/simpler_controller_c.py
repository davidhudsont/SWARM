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

class simple_drone_joy(object):
# define the default mapping between joystick buttons and their corresponding actions
	def __init__(self,name=""):
		rospy.init_node('ardrone_joystick_controller')
		self.ButtonEmergency = int (   rospy.get_param("~ButtonEmergency",ButtonEmergency) )
		self.ButtonLand      = int (   rospy.get_param("~ButtonLand",ButtonLand) )
		self.ButtonTakeoff   = int (   rospy.get_param("~ButtonTakeoff",ButtonTakeoff) )
		self.ButtonAuto		= int (	  rospy.get_param("~ButtonAuto",ButtonAuto) )
		self.ButtonThrsh		= int (   rospy.get_param("~ButtonThrsh",ButtonThrsh) )
		self.ButtonHighCon 	= int (	  rospy.get_param("~ButtonHighCon",ButtonHighCon) )
		self.AxisRoll        = int (   rospy.get_param("~AxisRoll",AxisRoll) )
		self.AxisPitch       = int (   rospy.get_param("~AxisPitch",AxisPitch) )
		self.AxisYaw         = int (   rospy.get_param("~AxisYaw",AxisYaw) )
		self.AxisZ           = int (   rospy.get_param("~AxisZ",AxisZ) )
		self.ScaleRoll       = float ( rospy.get_param("~ScaleRoll",ScaleRoll) )
		self.ScalePitch      = float ( rospy.get_param("~ScalePitch",ScalePitch) )
		self.ScaleYaw        = float ( rospy.get_param("~ScaleYaw",ScaleYaw) )
		self.ScaleZ          = float ( rospy.get_param("~ScaleZ",ScaleZ) )
		self.Group 			= str	( rospy.get_param("~Group",Group) )
		self.DroneID 		= str (rospy.get_param("~DroneID",DroneID) )
		self.ScaleRoll       = 1.0
		self.ScalePitch      = 1.0
		self.ScaleYaw        = 1.0
		self.ScaleZ          = 1.0
		self.DroneState = False
		self.thresh_state = False
		self.highcon_state = False
		self.Autodata = []
		self.phase = 0
		self.max_result = 400
		self.threshold = 1500
		self.axis = [0,0,0,0]
		self.direction = 1
		self.acelleration = 0.10
		self.id_index = 1
		DroneLogic(self)
		topic_name = Group+"/joy"
		subJoystick = rospy.Subscriber(topic_name, Joy, ReceiveJoystickMessage)
		
	def DroneLogic(self):
		if ( DroneID == 'FL') :
			self.id_index = 1
			self.direction = 1
		elif (DroneID == 'FR'):
			self.id_index = 0
			self.direction = -1
		elif (DroneID == 'RL'):
			self.id_index = 0
			self.direction = 1
		elif (DroneID == 'RR'):
			self.id_index = 1
			self.direction =  -1
		else :
			print("Not valid ID!!!!")
			self.id_index = 1
			self.direction  = 0

	def ReceiveJoystickMessage(self,data):
		rospy.loginfo("THR: %s, HGH: %s",self.thresh_state,self.highcon_state)
		if (DroneState == False):
			self.Autodata = []
			self.phase = 0
			if data.buttons[ButtonThrsh]==1:
				if (self.highcon_state == False and self.thresh_state == False):
					self.thresh_state = True
				else:
					self.thresh_state^= self.thresh_state
			elif data.buttons[self.ButtonHighCon]==1:
				if (self.thresh_state ==False and highcon_state == False):
					self.highcon_state = True
				else:
					self.highcon_state^= self.highcon_state
			elif data.buttons[self.ButtonEmergency]==1:
				#rospy.loginfo("Emergency Button Pressed")
				print("Emergency")
			elif data.buttons[self.ButtonLand]==1:
				#rospy.loginfo("Land Button Pressed")
				print("Landing")
			elif data.buttons[self.ButtonTakeoff]==1:
				#rospy.loginfo("Takeoff Button Pressed")
				print("Takeoff")
			else : 
				#controller.SetCommand(data.axes[AxisRoll]/ScaleRoll,data.axes[AxisPitch]/ScalePitch,data.axes[AxisYaw]/ScaleYaw,data.axes[AxisZ]/ScaleZ)
				print(data.axes)
				print(data.buttons)
		if (data.buttons[self.ButtonAuto]==1):
			DroneState ^= True

	def find_high_concentration(msg):
		#rospy.loginfo("Autodata: %s",Autodata)
		if (self.phase == 0):
			self.Autodata.append(msg.data)
			rospy.loginfo("Sweeping Out")
			if (len(self.Autodata) == 5):
				self.phase = 1
			self.axis[self.id_index] = self.acelleration*self.direction
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)	
		elif (self.phase == 1):
			self.max_result = max(self.Autodata)
			if ( abs(max_result-msg.data) < 100):
				self.phase = 2
			rospy.loginfo("Sweeping Back")
			self.axis[id_index] = self.acelleration*self.direction*-1
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
		elif (self.phase == 2):
			rospy.loginfo("Finished Phase 2")
			self.axis[self.id_index] = self.acelleration*self.direction*0
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
			self.phase = 3
		else:
			self.axis[self.id_index] = self.acelleration*self.direction*0
			#~ controller.SetCommand(axis[0]/ScaleRoll,axis[1]/ScalePitch,axis[2]/ScaleYaw,axis[3]/ScaleZ)		
			rospy.loginfo("Else State")
		
def follow_highest_concentration(msg):
	if (msg.data > self.max_result):
		self.max_result = msg.data
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

	#~ while(True):
		#~ i = 1
	#status = app.exec_()
	rospy.signal_shutdown('Great Flying!')
	sys.exit()
