"""Code modified from the example program to show how to read a multi-channel time series from LSL at https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py."""

from pylsl import StreamInlet, resolve_stream
import time  
import serial

# set up Arduino serial port - replace with the one you are using
ser = serial.Serial('COM4', 9600) 

# resolve an EMG stream on the lab network and notify the user
print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
#inlet_ch2 = StreamInlet(streams[1])
print("EMG stream found!")

# initialize time threshold and variables for storing time
thres = 500
prev_time = 0

while True:

	samples, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp

	curr_time = int(round(time.time() * 1000)) # get current time in milliseconds


	if ((samples[0] >=  0.7) & (curr_time - thres > prev_time)): # if an EMG spike is detected from the cheek muscles send 'G'
		prev_time = int(round(time.time() * 1000)) # update time 
		ser.write(b'G')


	elif((samples[1] >=  0.7) & (curr_time - thres > prev_time)): # if an EMG spike is detected from the eyebrow muscles send 'R'
		prev_time = int(round(time.time() * 1000)) # update time
		ser.write(b'R')

	elif(curr_time - thres > prev_time): # if no spike is detected send 'B'
		prev_time = int(round(time.time() * 1000)) # update time
		ser.write(b'B') 
