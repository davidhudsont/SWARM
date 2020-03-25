#!/usr/bin/env python
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
import random
from time import sleep
from std_msgs.msg import Int64
from std_msgs.msg import String
from std_msgs.msg import Empty       	 # for land/takeoff/emergency
import json

COMMAND_PERIOD = 1000
x = 2
y = 3
t = [False,False,False,False]

class Test(object):
	def __init__(self):
		rospy.init_node("test_node",anonymous=True)
		self.x 	= int (   rospy.get_param("~x",x) )
		self.y   = int (   rospy.get_param("~y",y) )
		self.t =  ( rospy.get_param("~t",t) )
		
		self.pubCoordinate = rospy.Publisher("/coord",String,queue_size=10)
		self.subCoordinate = rospy.Subscriber("/coord",String,self.GetCoordinate)
		#self.commandTimer = rospy.Timer(rospy.Duration(COMMAND_PERIOD/1000.0),self.SendCoordinate)
		
	def SendCoordinate(self):
		self.pubCoordinate.publish(self.PackJson())

	def PackJson(self):
		msg = {"x":self.x,"y":self.y,"t":self.t}
		js = json.dumps(msg)
		return  js
	
	def SetXY(self ,x,y,t):
		self.x = x
		self.y = y
		self.t = t
	
	def GetCoordinate(self,msg):
		rospy.loginfo("Coordinates: %s",msg.data)

if __name__=='__main__':
	#rospy.init_node("test_node",anonymous=True)
	# So we can init a node in a class
	# Can we put a launch file stuff in a class??
	# Yes we can awesome!!!!!!
	a = Test()
	#a.SetXY(2,3)
	
	while (True):
		a.SendCoordinate()
		sleep(1)
	
	rospy.signal_shutdown('Great Flying!')
	
