#!/usr/bin/env python



import rospy
from std_msgs.msg import String
# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
#from drone_controller import BasicDroneController
from sensor_msgs.msg import Joy
# This is a publisher node

# handles the reception of joystick packets
			
def auto_pub():
	rospy.init_node('autonomous_node', anonymous=True)
	sub = rospy.Subscriber("controller_node",int)
	rate = rospy.Rate(2)
	while not rospy.is_shutdown():
		if (DroneState ==1):
			print("Auto")
			rate.sleep()
		
		

if __name__=='__main__':
	try:
        auto_pub()
    except rospy.ROSInterruptException:
        pass
