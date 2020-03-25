#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from testing.msg import IntList
from std_msgs.msg import Int64
# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
#from drone_controller import BasicDroneController

# This is a publisher node

# handles the reception of joystick packets
import paho.mqtt.client as mqtt
import json

sensor_read = 0
ip = "192.168.1.104"
port = 1883

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("topic/test")


def on_message(client, userdata, msg):
	global sensor_read
	dat = ''
	m_decode = str(msg.payload.decode("utf-8", "ignore"))
	m_in = json.loads(m_decode)
	for key in m_in:
		for value in m_in[key]:
			dat = dat+value
		#print('dat',(int)(dat))
		sensor_read = (int)(dat)

def autonomous():
	global sensor_read
	global ip
	global port
	pub = rospy.Publisher('data',Int64,queue_size=10)
	rospy.init_node('autonomous', anonymous=True)
	broker_ip = (str) (rospy.get_param("~broker_ip",broker_ip))
	port = (int) (rospy.get_param("~port",port) )
	print(ip)
	print(port)
	
	client = mqtt.Client()
	#client.connect_async("192.168.1.107",1883,60)
	client.connect("192.168.1.104", 1883, 60)
	client.on_connect = on_connect
	client.on_message = on_message
	client.loop_start()
	
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		data = Int64()
		cmd = sensor_read
		print('sensor_read',cmd)
		data.data = cmd
		#rospy.loginfo(data)
		pub.publish(data)
		rate.sleep()
		
if __name__=='__main__':
	try:
		autonomous()
	except rospy.ROSInterruptException:
		pass
