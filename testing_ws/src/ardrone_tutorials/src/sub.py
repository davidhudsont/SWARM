#!/usr/bin/env python

import rospy
import time
#from std_msgs.msg import Int64
from std_msgs.msg import Int64
from std_msgs.msg import String


def callback(data):
	rospy.loginfo(data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('data', String, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
