#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64
import math
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy

import json
from time import sleep
from math import sin, cos, sqrt, atan2, radians
from PID_Controller import PID

class gps(object):
	def __init__(self,lat,lon):
		self.lat = lat
		self.lon = lon
		
	def gps_distance(self,lat1,lon1,lat2,lon2):
		R = 6373.0
		dlon = radians(lon2) - radians(lon1)
		print(dlon)
		dlat = radians(lat2) - radians(lat1)
		print(dlat)
		a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		print(a)
		print(c)
		distance = (R * c)*1000
		return distance


class imu(object):
	def __init__(self,rotZ):
		self.rotZ = rotZ
		self.axis = [0,0,0,0]
		self.p=PID(10.0,0.4,2.2)
		self.p.setPoint(180)
		self.min = self.p.update(180)
		self.max = self.p.update(0)

	def move_to_angle(self,dest):
		theta = dest-self.rotZ
		print(theta)
		C = 2*math.pi
		if (abs(self.rotZ-dest) < 5):
			axis = [0,0,0,0]
		elif (theta < 0):
			L1 = theta/180.0*math.pi*-1
			L2 = C-L1
			print(L1,L2)
			if (L2<L1):
				deg = 360+theta
				print(deg)
				# speed = self.map(deg,0.0,180.0,0.0,1.0)
				speed = deg/180.0
				self.axis = [0,0,speed,0]
			else:
				print(theta)
				# speed = self.map(abs(theta),0.0,180.0,0.0,-1.0)
				speed = theta/180.0
				self.axis = [0,0,speed,0]
		else :
			L1 = theta/180.0*math.pi
			L2 = 2*math.pi-L1
			print(L1,L2)
			if (L2<L1):
				deg = theta-360
				print(deg)
				# speed = self.map(deg,0.0,180.0,0.0,-1.0)
				speed = deg/180.0
				self.axis = [0,0,speed,0]
			else:
				# speed = self.map(theta,0.0,180.0,0.0,1.0)
				speed = theta/180.0
				self.axis = [0,0,speed,0]
		print(self.axis)	

	def pid_move_to_angle(self,dest):
		theta = dest-self.rotZ
		print(theta)
		C = 2*math.pi
		if (abs(self.rotZ-dest) < 5):
			axis = [0,0,0,0]
		elif (theta < 0):
			L1 = theta/180.0*math.pi*-1
			L2 = C-L1
			print(L1,L2)
			if (L2<L1):
				deg = 360+theta
				print(deg)
				pid = self.p.update(deg)
				print("Stuff",pid,self.max,self.min)
				speed = self.map(pid,self.max,self.min,0.0,1.0)
				self.axis = [0,0,speed,0]
			else:
				print(theta)
				# speed = self.map(abs(theta),0.0,180.0,0.0,-1.0)
				pid = self.p.update(theta)
				speed = self.map(pid,self.max,self.min,0.0,1.0)
				speed = theta/180.0
				self.axis = [0,0,speed,0]
		else :
			L1 = theta/180.0*math.pi
			L2 = 2*math.pi-L1
			print(L1,L2)
			if (L2<L1):
				deg = theta-360
				self.p.setPoint(180)
				pid = self.p.update(deg)
				print("PID",pid)
				print(deg)
				# speed = self.map(deg,0.0,180.0,0.0,-1.0)
				speed = deg/180.0
				self.axis = [0,0,speed,0]
			else:
				# speed = self.map(theta,0.0,180.0,0.0,1.0)
				self.p.setPoint(180)
				pid = self.p.update(theta)
				print("PID",pid)
				speed = theta/180.0
				self.axis = [0,0,speed,0]
		print(self.axis)
		

	def map(self, x, in_min, in_max, out_min, out_max) :
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

# 0 is axis roll (left and right)
# 1 is axis pitch (forward and backward)
# 2 is axis yaw (rotate left and right)
# 3 is axis z (vertical up and down)

COMMAND_PERIOD = 1000 #ms

class drone(object):
	def __init__(self,name="ardrone1",tag="FL",threshold=1500,acceleration=0.1):
		self.ws = 0
		self.wa = 0
		self.co2 = 400
		self.axis = [0,0,0,0]
		self.phase = 0
		self.lat = 0
		self.lon = 0
		self.tag = tag
		self.altitude = -1
		self.auto_state = False
		self.Autodata = []
		self.threshold = threshold
		self.acceleration = acceleration
		self.direction = 0
		self.id_index = 0
		self.rotZ = 0
		self.name = name
		self.bat = -1
		self.angle = 90
		self.start_alt = 700

		self.drone_id_logic()
		# Subscribers
		self.subControllerFeedback = rospy.Subscriber(name+'/ardrone/controller',String,self.recieveFeeback)
		self.subSensorData = rospy.Subscriber(name+'/ardrone/data',String,self.receiveSensor)
		
		# Publihsers
		self.pubCommand = rospy.Publisher(name+'/ardrone/commands',String,queue_size=10)		
		
	def recieveFeeback(self, msg):
		js = json.loads(msg.data)
		self.ws = js["ws"]
		self.wa = js["wa"]
		self.auto_state = js["state"]
		self.bat = js["bat"]
		self.rotZ = js["rotZ"]
		self.altitude = js["alt"]
		# self.angle = js["angle"]
		
	def receiveSensor(self, msg):
		js = json.loads(msg.data)
		self.lat = js["lat"]
		self.lon = js["lon"]
		self.co2 = js["co2"]
	
	def publishCommands(self):
		js = {"axis":self.axis}
		msg = json.dumps(js)
		self.pubCommand.publish(msg)
	
	def drone_id_logic(self):
		DroneID = self.tag
		if ( DroneID == 'FL') :
			self.id_index = 1
			self.direction = 1.0
			self.acceleration = 0.15
		elif (DroneID == 'FR'):
			self.id_index = 0
			self.direction = -1.0
		elif (DroneID == 'RL'):
			self.acceleration = 0.1
			self.id_index = 0
			self.direction = 1.0
		elif (DroneID == 'RR'):
			self.acceleration = 0.15
			self.id_index = 1
			self.direction =  -1.0
		else :
			print("Not valid ID!!!!")
			self.id_index = 1
			self.direction  = 0
		
	def threshold_find(self):
		# rospy.loginfo("Sweeping Out")
		self.Autodata.append(self.co2)
		rospy.loginfo("Autodata : %s",self.Autodata)
		if (abs(self.co2-self.threshold) <= 500):
			rospy.loginfo("Found Threshold")
			self.axis[self.id_index] = self.acceleration*self.direction*0.0
			self.phase += 1
		elif (len(self.Autodata) == 5):
			rospy.loginfo("Reached end of sweep")
			self.axis[self.id_index] = self.acceleration*self.direction*0.0
			self.phase += 1
		else:
			self.axis[self.id_index] = self.acceleration*self.direction
		rospy.loginfo("axis: %s",self.axis)
		self.publishCommands()

	def threshold_track(self):
		rospy.loginfo("Tracking Mode")
		self.axis = [0,0.1,0,0]
		self.publishCommands()
	
	def reset_auto(self):
		self.phase = 0
		self.Autodata = []
	

	def rotate_to_angle(self,dest):
		theta = dest-self.rotZ
		print(theta)
		if (dest == 0  and (abs(360-self.rotZ) < 15 ) or (abs(0 - self.rotZ)<15)):
			self.axis = [0,0,0,0]
			self.phase += 1
		elif (abs(theta) < 15):
			self.axis = [0,0,0,0]
			self.phase += 1
		elif (theta < 0):
			L1 = theta/180.0*math.pi
			L2 = 2*math.pi-L1
			# print(L1,L2)
			if (L2<L1):
				self.axis = [0,0,1,0]
			else:
				self.axis = [0,0,-1,0]
		else :
			L1 = theta/180.0*math.pi
			L2 = 2*math.pi-L1
			# print(L1,L2)
			if (L2<L1):
				self.axis = [0,0,-1,0]
			else:
				self.axis = [0,0,1,0]
		self.publishCommands()
		# print(self.axis)		
			
		
	def rotate_to_angle_variable(self,dest):
		theta = dest-self.rotZ
		# print(theta)
		C = 2*math.pi
		if (dest == 0  and (abs(360-self.rotZ) < 3.5 ) or (abs(0 - self.rotZ)<5)):
			self.axis = [0,0,0,0]
			self.phase += 1
		elif (abs(theta) < 5):
			self.axis = [0,0,0,0]
			self.phase += 1
		elif (theta < 0):
			L1 = theta/180.0*math.pi*-1
			L2 = C-L1
			# print(L1,L2)
			if (L2<L1):
				deg = 360+theta
				# print(deg)
				speed = self.map(deg,0.0,180.0,0.1,1.0)
				# speed = deg/180.0
				self.axis = [0,0,speed,0]
			else:
				# print(theta)
				speed = self.map(abs(theta),0.0,180.0,-0.1,-1.0)
				# speed = theta/180.0
				self.axis = [0,0,speed,0]
		else :
			L1 = theta/180.0*math.pi
			L2 = 2*math.pi-L1
			# print(L1,L2)
			if (L2<L1):
				deg = theta-360
				# print(deg)
				speed = self.map(deg,0.0,180.0,-0.1,-1.0)
				# speed = deg/180.0
				self.axis = [0,0,speed,0]
			else:
				speed = self.map(theta,0.0,180.0,0.1,1.0)
				# speed = theta/180.0
				self.axis = [0,0,speed,0]
		# rospy.loginfo("Rotation Speed: %s",self.axis)
		self.publishCommands()
		# print(self.axis)

	def raise_to_altitude(self,alt,max_alt):
		if (abs(self.altitude-alt) < 100):
			self.phase +=1
			self.axis = [0,0,0,0]
			# rospy.loginfo("Reached correct Altitude")
		elif (self.altitude < alt):
			# rospy.loginfo("Raising to correct Altitude")
			speed = self.map(self.altitude,alt,700,0.1,1.0)
			self.axis = [0,0,0,speed]
		else :
			speed = self.map(self.altitude,alt,max_alt,-0.1,-1.0)
			self.axis = [0,0,0,speed] 
			# rospy.loginfo("Lowering to correct Altitude")
		self.publishCommands()
	
	def map(self, x, in_min, in_max, out_min, out_max) :
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

	def hover(self):
		self.axis = [0,0,0,0]
		self.publishCommands()
