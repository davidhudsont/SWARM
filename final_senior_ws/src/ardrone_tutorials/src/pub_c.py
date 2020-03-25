#!/usr/bin/env python

import rospy
import random
#from std_msgs.msg import Int64
#from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Int64
from std_msgs.msg import String
import json

tags = ["RL","RR","FL","FR"]
nodes = []
node_count = 0



def talker():
	global nodes
	global node_count
	node_count = int (   rospy.get_param("~node_count",node_count) )
	Group = str ( rospy.get_param("~Group",Group) )
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
