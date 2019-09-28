#!/usr/bin/env python

import rospy

#from std_msgs.msg import Int64
#from std_msgs.msg import Int64MultiArray
from testing.msg import IntList

def talker():
	pub = rospy.Publisher('data', IntList, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(2)
	while not rospy.is_shutdown():
		data = IntList()
		data.data = [1,2,3]
		rospy.loginfo(data)
		pub.publish(data)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
