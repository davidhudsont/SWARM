#!/usr/bin/env python
import exceptions
from time import sleep
import sys
import os
import roslaunch

import rospy

import roslaunch

# uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
# roslaunch.configure_logging(uuid)

# cli_args = ['class_testing', 'master.launch', 'd1:=true', 'd2:=false']
# roslaunch_file = roslaunch.rlutil.resolve_launch_arguments(cli_args)
# roslaunch_args = cli_args[2:]

# parent = roslaunch.parent.ROSLaunchParent(uuid, [(roslaunch_file, roslaunch_arg)])

# parent.start()

import roslaunch

rospy.init_node('en_Mapping', anonymous=True)
rospy.on_shutdown(self.shutdown)

uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/viki/testing_ws/src/class_testing/launch/master.launch"])

launch.start()

launch.shutdown()