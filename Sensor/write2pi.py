import serial
import time

ser = serial.Serial('/dev/ttyS2',115200)

while True:
	ser.write('Hello\n')
	print(1)
	time.sleep(1)
	
