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
	rospy.init_node('pub', anonymous=True)
	node_count = int (   rospy.get_param("~node_count",node_count) )
	tag = str ( rospy.get_param("~tag",tag) )
	pub = rospy.Publisher("/data/"+tag, String, queue_size=10)
	rate = rospy.Rate(1)
	
	while not rospy.is_shutdown():
		msg = String()
		data = random.randint(400,8000)
		js = {"tag":tag, "CO2":data}
		msg = json.dumps(js)
		rospy.loginfo("Sent: %s",msg)
		pub.publish(msg)
		rate.sleep()

def multi_talker():
	global nodes
	global node_count
	rospy.init_node('pub', anonymous=True)
	node_count = int (   rospy.get_param("~node_count",node_count) )
	for n in range(node_count):
		tmp = rospy.Publisher("/data/"+tags[n], String, queue_size=10)
		nodes.append(tmp)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		for n in range(node_count):
			msg = String()
			data = random.randint(400,8000)
			js = {"tag":tags[n], "CO2":data}
			msg = json.dumps(js)
			rospy.loginfo("Sent: %s",msg)
			nodes[n].publish(msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
