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
# Import the joystick message
import time 
import threading
# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display

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
init_sweep = False
t_beg = 0
max_result = 400

def AutoCallback(data):
	rospy.loginfo("Recieved %s", data.data)
	
class Runnable(QtCore.QRunnable):
	
	def run(self):
		app = QtCore.QCoreApplication.instance()
		rospy.Subscriber("data", Int64, AutoCallback)
		rospy.loginfo("Begin communication with Autonomous Node")
		while (True):
			rospy.sleep(1)
		app.quit()
	

def main_window():
	app = QtGui.QApplication(sys.argv)
	runnable = Runnable()
	QtCore.QThreadPool.globalInstance().start(runnable)
	window = QtGui.QWidget()
	window.setGeometry(0, 0, 500, 300)
	window.setWindowTitle("PyQT Tuts!")
	window.show()
	status = app.exec_()
	rospy.signal_shutdown('Great Flying!')
	rospy.loginfo("Shutting Down!!!!")
	sys.exit(status)

# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('ardrone_joystick_controller')
	
	main_window()
