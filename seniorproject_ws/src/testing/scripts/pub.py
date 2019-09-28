#!/usr/bin/env python

import rospy
import random
#from std_msgs.msg import Int64
#from std_msgs.msg import Int64MultiArray
from testing.msg import IntList
from std_msgs.msg import Int64


node_name = "pub1"

def talker():
	
	pub = rospy.Publisher('data', Int64, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		data = Int64()
		data.data = random.randint(400,1200)
		rospy.loginfo("Sent: %s",data.data)
		pub.publish(data)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
