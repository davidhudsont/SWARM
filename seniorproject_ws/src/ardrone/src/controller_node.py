#!/usr/bin/env python

# The Joystick Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Joystick Control"
# https://github.com/mikehamer/ardrone_tutorials

# This controller implements the base DroneVideoDisplay class, the DroneController class and subscribes to joystick messages

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
import time
# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay

# Import the joystick message
from sensor_msgs.msg import Joy
from std_msgs.msg import Int64
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

DroneState = False
Autodata = []
init_sweep = 0
t_beg = 0

# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	global DroneState
	global t_beg 
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
		else : 
			#controller.SetCommand(data.axes[AxisRoll]/ScaleRoll,data.axes[AxisPitch]/ScalePitch,data.axes[AxisYaw]/ScaleYaw,data.axes[AxisZ]/ScaleZ)
			print("Axes ",data.axes)
	if (data.buttons[ButtonAuto]==1):
		DroneState ^= True
		t_beg = time.clock()
		#print("Autonomous, DroneState: ", DroneState)
		#print("Autodata: ",Autodata)

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
	if (init_sweep == 0):
		if (len(Autodata) < 5):
			init_sweep = 1
		Autodata.append(data.data)
		#controller.SetCommand(0.0/ScaleRoll,0.25/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)	
	elif (init_sweep == 1):
		tmp = max(Autodata)
		if ( abs(tmp-data.data) < 30)
			init_sweep = 2
		#controller.SetCommand(0.0/ScaleRoll,-0.25/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
	elif (init_sweep == 2):
		#controller.SetCommand(0/ScaleRoll,0.0/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
	else:
		#controller.SetCommand(0/ScaleRoll,0.0/ScalePitch,0.0/ScaleYaw,0.0/ScaleZ)
		print(Autodata)

def AutoCallback(data):
	global Autodata
	global DroneState
	global init_sweep
	global t_beg
	if (DroneState == True):
		rospy.loginfo("Autonomous %s", data.data)
		phase_1(data)
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

	# Now we construct our Qt Application and associated controllers and windows
	app = QtGui.QApplication(sys.argv)
	display = DroneVideoDisplay()
	controller = BasicDroneController()

	# subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	subJoystick = rospy.Subscriber('/joy', Joy, ReceiveJoystickMessage)
	
	# executes the QT application
	display.show()
	status = app.exec_()
	subJoystick = rospy.Subscriber('/joy', Joy, ReceiveJoystickMessage)
	listener()
	# and only progresses to here once the application has been shutdown
	rospy.signal_shutdown('Great Flying!')
	sys.exit(status)
