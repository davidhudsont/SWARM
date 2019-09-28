#!/usr/bin/env python

import rospy
import time
#from std_msgs.msg import Int64
from testing.msg import IntList
from std_msgs.msg import Int64



def callback(data):
	rospy.loginfo(data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('chatter', Int64, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
