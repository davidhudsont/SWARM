#!/usr/bin/env python

import rospy
import random
#from std_msgs.msg import Int64
#from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Int64
from std_msgs.msg import String
import json

node_name = "pub1"
tags = ["RL","RR","FL","FR"]
nodes = []
node_count = 0
tag = "FL"


def talker():
	global nodes
	global node_count
	global tag
	pub = rospy.Publisher("ardrone1/ardrone/controller", String, queue_size=10)
	rate = rospy.Rate(1)
	
	while not rospy.is_shutdown():
		msg = String()
		Auto = False
		ws = 0.231
		wa = -34.34
		js = {"tag":tag, "auto":Auto,"ws":ws,"wa":wa}
		msg = json.dumps(js)
		rospy.loginfo("Sent: %s",msg)
		pub.publish(msg)
		rate.sleep()

def callback(msg):
	rospy.loginfo("Msg: %s",msg)

def reciever():
	global tag
	rospy.init_node('controller', anonymous=True)
	tag = str ( rospy.get_param("~tag",tag) )
	sub = rospy.Subscriber("ardrone1/ardrone/commands", String, callback)
	
	

if __name__ == '__main__':
	try:
		reciever()
		talker()
	except rospy.ROSInterruptException:
		pass
