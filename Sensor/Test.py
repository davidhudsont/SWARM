import serial
import time


ser = serial.Serial("/dev/ttyS0',57600)

while True:
	print(ser.readline())
	