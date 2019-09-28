#!/usr/bin/env python

from beginner_tutorials.srv import *
import rospy

def handle_server(req):
    ret = str(req.a)+", "+str(req.b)
    print "Returning [%s , %s = %s]"%(req.a, req.b, ret)
    return testResponse(ret)

def add_two_ints_server():
    rospy.init_node('test_server')
    s = rospy.Service('testing', test, handle_server)
    print "Ready to return a string."
    rospy.spin()

if __name__ == "__main__":
    add_two_ints_server()
