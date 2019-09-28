#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64

import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy

import json
from time import sleep



class gps(object):
	def __init__(self):
		self.lat = 0
		self.lon = 0
		
	def set_lat_long(self,lat,lon):
		self.lat = lat
		self.lon = lon

	def get_lat_long(self):
		return [self.lat,self.lon]

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
		self.auto_state = False
		self.Autodata = []
		self.threshold = threshold
		self.acceleration = acceleration
		self.direction = 0
		self.id_index = 0
		self.name = name
		self.drone_id_logic()
		
		# Subscribers
		self.subControllerFeedback = rospy.Subscriber(name+'/ardrone/controller',String,self.recieveFeeback)
		self.subSensorData = rospy.Subscriber(name+'/ardrone/data',String,self.receiveSensor)
		
		# Publihsers
		self.pubCommand = rospy.Publisher(name+'/ardrone/commands',String,queue_size=10)
		
		# Setup regular publishing of control packets
		#self.rate = rospy.Rate(1)
		
		
	def recieveFeeback(self, msg):
		js = json.loads(msg.data)
		self.ws = js["ws"]
		self.wa = js["wa"]
		self.auto_state = js["state"]
		
	def receiveSensor(self, msg):
		js = json.loads(msg.data)
		self.lat = js["latitude"]
		self.lon = js["longitude"]
		self.co2 = js["CO2"]
	
	def publishCommands(self):
		js = {"axis":self.axis}
		msg = json.dumps(js)
		self.pubCommand.publish(msg)
	
	def drone_id_logic(self):
		DroneID = self.tag
		if ( DroneID == 'FL') :
			self.id_index = 1
			self.direction = 1
		elif (DroneID == 'FR'):
			self.id_index = 0
			self.direction = -1
		elif (DroneID == 'RL'):
			self.id_index = 0
			self.direction = 1
		elif (DroneID == 'RR'):
			self.id_index = 1
			self.direction =  -1
		else :
			print("Not valid ID!!!!")
			self.id_index = 1
			self.direction  = 0
		
	def threshold_find(self):
		if (self.phase == 0):
			rospy.loginfo("Sweeping Out")
			self.Autodata.append(self.co2)
			rospy.loginfo("Autodata : %s",self.Autodata)
			if (abs(self.co2-self.threshold) <= 500):
				rospy.loginfo("Found Threshold")
				self.axis[self.id_index] = self.acceleration*self.direction*0
				delay = 5-len(self.Autodata) 
				self.publishCommands()
				sleep(delay)
				self.phase = 1
			elif (len(self.Autodata) == 5):
				rospy.loginfo("Reached end of sweep")
				self.axis[self.id_index] = self.acceleration*self.direction*0
				self.publishCommands()
				self.phase = 1
			else:
				self.axis[self.id_index] = self.acceleration*self.direction
				self.publishCommands()

	def threshold_track(self):
		rospy.loginfo("Currently does nothing")
		self.axis[self.id_index] = self.acceleration*self.direction*0
		self.publishCommands()
	
	def reset_auto(self):
		self.phase = 0
	
	def run(self):
		if (self.auto_state):
			if (self.phase == 1):
				self.threshold_track()
			else: 
				self.threshold_find()
		else :
			self.reset_auto()
			
			
			
		
