#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64

# This is an Autonoumous publisher node

# MQTT and Json
import paho.mqtt.client as mqtt
import json

# Global values
sensor_read = 100
broker_ip = "192.168.1.150"
port = 1883
tag = "FR"
topic = "Drone/"

sim =[514,750,1014,823,423,   # Sweep out
	  414,798,989,1000,700,   # Sweep back
	  720,800,814,690,690]   # 


def autonomous():
	global sensor_read
	global broker_ip
	global port
	global topic
	global sim
	pub = rospy.Publisher('data',Int64,queue_size=10) 			# Construct publisher
	rospy.init_node('autonomous', anonymous=True) 				# Initialize node
	rate = rospy.Rate(1) 				# Set rate of publishing messages to 1 second
	time = 0
	while not rospy.is_shutdown():
		msg = Int64() 									# ros_msg constructor
		if (time >= len(sim)) :
			msg.data = sim[len(sim)-1]
		else :
			msg.data = sim[time] 							# attach sensor data to the msg
		pub.publish(msg) 								# Publish the data
		rospy.loginfo("Sent : %s",msg.data)
		time +=1
		rate.sleep() 									# Sleep for 1 second
		
if __name__=='__main__':
	try:
		autonomous() # Try to Initialize the ROS node
	except rospy.ROSInterruptException:
		pass
