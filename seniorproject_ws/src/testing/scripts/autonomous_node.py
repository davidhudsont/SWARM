#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64


# This is a Autonoumous publisher node

# MQTT and Json
import paho.mqtt.client as mqtt
import json

# Global values
sensor_read = 400
broker_ip = "192.168.1.104"
port = 1883
tag = "FR"
topic = "Drone/FL"

def on_connect(client, userdata, flags, rc):
	global tag
	print("Connected with result code " + str(rc))
	tag = (str) (rospy.get_param("~tag",tag))
	topic = "Drone/"+tag
	print(topic)
	client.subscribe(topic)


def on_message(client, userdata, msg):
	global sensor_read
	m_decode = str(msg.payload.decode("utf-8", "ignore")) # Recieve and decode message from MQTT
	msg_r = json.loads(m_decode) # Decode message into json object
	sensor_read = msg_r["CO2"] # Access CO2 data 

def autonomous():
	global sensor_read
	global broker_ip
	global port
	global topic
	pub = rospy.Publisher('data',Int64,queue_size=10) 			# Construct publisher
	rospy.init_node('autonomous', anonymous=True) 				# Initialize node
	broker_ip = (str) (rospy.get_param("~broker_ip",broker_ip)) # Get IP from launch file
	port = (int) (rospy.get_param("~port",port) ) 				# Get port from launch file
	print("Connecting to Broker IP: ",broker_ip) 
	print("Through port: ",port)
	
	client = mqtt.Client() 				# Contstructor
	client.connect(broker_ip, port,60) # Connect to MQTT broker
	client.on_connect = on_connect 		# Add connect function
	client.on_message = on_message		# Add message recieve function
	client.loop_start()	 				# Start Recieving messages 
	rate = rospy.Rate(1) 				# Set rate of publishing messages to 1 second
	
	while not rospy.is_shutdown():
		msg = Int64() 									# ros_msg constructor
		msg.data = sensor_read 							# attach sensor data to the msg
		rospy.loginfo("Sending Data:  %s %s", topic,msg.data) 	# Log the info
		pub.publish(msg) 								# Publish the data
		rate.sleep() 									# Sleep for 1 second
		
if __name__=='__main__':
	try:
		autonomous() # Try to Initialize the ROS node
	except rospy.ROSInterruptException:
		pass
