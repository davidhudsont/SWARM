#!/usr/bin/env python
import rospy
import time
import random
#from std_msgs.msg import Int64
from std_msgs.msg import Int64
from std_msgs.msg import String

import json

from sensors import drone
import roslaunch

navdata = []
drones = []
sensors = []
coms = []
node_count = 0
tags = ["FL","FR","RL","RR"]

max_result = 400
threshold = 1500

def callback(msg):
	js = json.loads(msg.data)
	#rospy.loginfo("Recieved Message: %s", js)
	if (js["tag"]=="FL"):
		rospy.loginfo("Recieved FL: %s",js["CO2"])
	elif (js["tag"]=="FR"):
		rospy.loginfo("Recieved FR: %s",js["CO2"])
	elif (js["tag"]=="RL"):
		rospy.loginfo("Recieved RL: %s",js["CO2"])		
	elif (js["tag"]=="RR"):
		rospy.loginfo("Recieved RR: %s",js["CO2"])

def control(msg):
	js = json.loads(msg.data)
	#rospy.loginfo("Recieved Message: %s", js)
	if (js["tag"]=="FL"):
		rospy.loginfo("Recieved FL: %s",js["ws"])
	elif (js["tag"]=="FR"):
		rospy.loginfo("Recieved FR: %s",js["ws"])
	elif (js["tag"]=="RL"):
		rospy.loginfo("Recieved RL: %s",js["ws"])		
	elif (js["tag"]=="RR"):
		rospy.loginfo("Recieved RR: %s",js["ws"])
	

def multi_listener():
	global node_count
	global sensors
	global navdata
	rospy.init_node('listener', anonymous=True)
	node_count = int (   rospy.get_param("~node_count",node_count) )
	for n in range(node_count):
		tmp = rospy.Subscriber("/data/"+tags[n], String, callback)
		sensors.append(tmp)
		tmp = rospy.Subscriber("/state/"+tags[n], String, control)
		drones.append(tmp)
	#rospy.spin()
	

def commands():
	global node_count
	global coms
	
	for n in range(node_count):
		tmp = rospy.Publisher("/commands/"+tags[n], String, queue_size=10)
		coms.append(tmp)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		for n in range(node_count):
			msg = String()
			axis = [0.424,0.34,0,0]
			js = {"tag":tags[n], "Axis":axis}
			msg = json.dumps(js)
			rospy.loginfo("Sent: %s",msg)
			coms[n].publish(msg)
		rate.sleep() 

if __name__ == '__main__':
	rospy.init_node('master', anonymous=True)
	d0 = drone("ardrone1","FL")
	d1 = drone("ardrone2","RR")
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		d0.run()
		d1.run()
		rate.sleep()
	#~ multi_listener()
	#~ commands()
