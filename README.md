# SWARM

## Latest Code
* Latest Arduino Code for Linkit is under https://github.com/davidhudsont/Senior_Project_SWARM/tree/master/Linkit_Publish/Linkit_Sensor_GPS
* Latest MQTT Python Microprocessor Code is at
https://github.com/davidhudsont/Senior_Project_SWARM/tree/master/Linkit_Publish


## ROS VM Final Code Location
* Final workspace is workspace_testing.sh
* The final code is located in testing_ws/src/ardrone_tutorials/
* Final Code in /src
  * master_node.py, controller_node.py, autonmous_node.py
* Final XML in /launch
  * master_ardrone.launch, controller_auto.launch

## Ardrone ROS User Guide
* Start a ROS workspace
  * source /bin/'name of workspace.sh'
  * workspace names are found in /home/viki/bin
  * naming scheme : workspace_*.sh
  * You then can use the ros utilities such as roslaunch
 
## Launching ArDrone
* open the terminal
* Setup ROS Workspace
  * source /bin/workspace_testing_ws
* open up the master_adrone.launch
  * subl testing_ws/src/ardrone_tutorials/launch/master_ardrone.launch
* set the flags to drone flags to true or false to connect a drone
![alt text][logo7]

[logo7]: https://github.com/davidhudsont/Senior_Project_SWARM/blob/master/Images/DroneFlying_Tutorial_02.jpg "Drone Flags"
* Then connect to dronenet and use roslaunch to launch the ArDrone
  * roslaunch ardrone_tutorials master_ardrone.launch 
* The controls are listed below

# Ardrone Controls PS4
* Left Stick = Forwards, Backwards, Left & Right
* Right Stick = Rotation, Up & Down
* X Button = Liftoff
* Square Button = Emergency Land
* Triangle Button = Autonomous Mode
* Circle Button = Land
* D-pad = Disables/enables manual control of drones from left to down clockwise = FL,FR,RL,RR Drones (Should be)
 

## Resources :
* https://github.com/AutonomyLab/ardrone_autonomy
* http://www.instructables.com/id/Autonomous-AR-Parrot-Drone-20-Flying/
* http://wiki.ros.org/ardrone_autonomy
* https://pypi.org/project/paho-mqtt/
* https://github.com/AutonomyLab/ardrone_autonomy/wiki/Multiple-AR-Drones
* https://nootrix.com/diy-tutos/ros-indigo-virtual-machine/

## Sensor Unit
* http://wiki.seeedstudio.com/LinkIt_Smart_7688_Duo/
* https://www.sparkfun.com/products/14193
* https://www.sparkfun.com/products/14414



## ROS Diagrams

![alt text][logo]

[logo]: https://github.com/davidhudsont/SWARM/blob/master/Images/Master_1_Ardrone.PNG "1 Ardrone"

![alt text][logo2]

[logo2]: https://github.com/davidhudsont/SWARM/blob/master/Images/Master_2_Ardrone.PNG "2 Ardrones"

## Prototype

### System Overview
![alt text][logo3]

[logo3]: https://github.com/davidhudsont/SWARM/blob/master/Images/Pictograph_System.jpg "System Overview"


![alt text][logo4]

[logo4]: https://github.com/davidhudsont/SWARM/blob/master/Images/030.jpg "4 Drone Swarm Prototypes"

![alt text][logo5]

[logo5]: https://github.com/davidhudsont/SWARM/blob/master/Images/032.jpg "Drone Prototype Closeup"

![alt text][logo6]

[logo6]: https://github.com/davidhudsont/SWARM/blob/master/Images/024.jpg "Sensor Unit Prototype Closeup"

