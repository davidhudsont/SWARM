#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def testing_client(x, y):
    rospy.wait_for_service('testing')
    try:
        func = rospy.ServiceProxy('testing', test)
        resp1 = func(x, y)
        return resp1.ret
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    x = 2
    y = 5
    print "Requesting %s+%s"%(x, y)
    counter = 10
    while (counter >0):
		print "%s , %s = %s"%(x, y, testing_client(x, y))
		counter -= 1
