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
Group = "ardrone1"

def talker():
	global nodes
	global node_count
	global tag
	global Group
	pub = rospy.Publisher(Group+"/ardrone/controller", String, queue_size=10)
	rate = rospy.Rate(1)
	
	while not rospy.is_shutdown():
		msg = String()
		Auto = True
		ws = 0.231
		wa = -34.34
		js = {"tag":tag, "state":Auto,"ws":ws,"wa":wa}
		msg = json.dumps(js)
		rospy.loginfo("Sent: %s",msg)
		pub.publish(msg)
		rate.sleep()

def callback(msg):
	js = json.loads(msg.data)
	rospy.loginfo("Commands : %s",msg)
	axis = js["axis"]
	print("Commands: ",axis[1])
	

def reciever():
	global tag
	global Group
	rospy.init_node('controller', anonymous=True)
	tag = str ( rospy.get_param("~tag",tag) )
	Group = str ( rospy.get_param("~Group",Group) )
	sub = rospy.Subscriber(Group+"/ardrone/commands", String, callback)
	
	

if __name__ == '__main__':
	try:
		reciever()
		talker()
	except rospy.ROSInterruptException:
		pass
