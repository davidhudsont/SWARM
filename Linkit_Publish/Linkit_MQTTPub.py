from time import sleep
import paho.mqtt.client as mqtt
import json
import serial
import time
import socket
import sys

print("Version 1.00")
'''
	Version 1.00 Linkit_MQTTPub
	
	Authors: David Hudson, David Vercillo
	
	This python script is designed to read from the serial port of the 
	linkit arduino mcu and recieve sensor data and publish the data
	to MQTT topics.

'''
# Attempt to connect to MQTT Broker
ip = "192.168.1.150"
ser = serial.Serial(port="/dev/ttyS0",baudrate=57600,timeout=2)
try :
	client = mqtt.Client()
	client.connect(ip, 1883, 60)
except (socket.error):
	print("Error! RPi is unplugged!")
	sys.exit()

drone_id = 0
tag = ["FL","FR","RL","RR"]
topic = "Drone/"+tag[drone_id]

print(topic)

while True:
	try:
		json_data = ser.readline()
		json_obj = json.loads(json_data)
		json_obj['id'] = drone_id
		json_obj['time'] = time.time()
		json_data = json.dumps(json_obj)
		print(json_data)
		client.publish(topic, json_data)
		# sleep(1)
	except(ValueError,TypeError):
		print("String from arduino is incomplete!!!")
		pass
	except(KeyboardInterrupt, socket.error, SystemExit):
		print("Exiting!")
		ser.close()
		client.disconnect()
		sys.exit()