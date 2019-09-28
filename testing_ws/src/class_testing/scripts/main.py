#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64
from sensors import drone

if __name__ == '__main__':
	
	d = drone("RR",1000,0.3)
	d.print_data()
	s = String()
	s.data = 400
	print(s)
	d.threshold_find(s)
	d.threshold_track(s)
	print(d.get_commands())
