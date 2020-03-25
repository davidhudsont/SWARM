#!/usr/bin/env python
import rospy
import time
import random
#from std_msgs.msg import Int64
from std_msgs.msg import Int64
from std_msgs.msg import String

import json

navdata = []
sensors = []
coms = []
node_count = 0
node_list = [False,False,False,False]
tags = ["FL","FR","RL","RR"]

max_result = 400
threshold = 1500

def sensor_callback(msg):
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
	global node_list
	rospy.init_node('listener', anonymous=True)
	node_list =  rospy.get_param("~node_list",node_list)
	count = 0
	for n in (node_list):
		if (n=="T"):
			tmp = rospy.Subscriber("/data/"+tags[count], String, sensor_callback)
			sensors.append(tmp)
			tmp = rospy.Subscriber("/state/"+tags[count], String, control)
			navdata.append(tmp)
		count = count + 1
	#rospy.spin()
	

def commands():
	global coms
	global node_list
	global node_count
	count = 0
	for n in node_list:
		if (n=="T"):
			tmp = rospy.Publisher("/commands/"+tags[count], String, queue_size=10)
			coms.append(tmp)
		count = count + 1
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		count = 0
		for n in coms:
			msg = String()
			axis = [0.424,0.34,0,0]
			js = {"tag":tags[count], "Axis":axis}
			msg = json.dumps(js)
			rospy.loginfo("Sent: %s",msg)
			n.publish(msg)
			count = count+1
		rate.sleep() 

if __name__ == '__main__':
	multi_listener()
	commands()
