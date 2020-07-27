"""Code modified from the example program to show how to read a multi-channel time series from LSL at https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py."""

from pylsl import StreamInlet, resolve_stream
import pyautogui
import time  

# resolve an EMG stream on the lab network and notify the user
print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

# initialize thresholds and variables for storing time 
prev_time = 0
flex_thres = 1.0

while True:

	sample, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp

	curr_time = int(round(time.time() * 1000)) # get current time in milliseconds


	if (((sample[1] >= flex_thres) or (sample[0] >= flex_thres))): # if an EMG peak is detected from any of the arms 

		prev_time = int(round(time.time() * 1000)) # update time 
		
		if(sample[1] > sample[0]): # scroll up or down depending on which peak is larger
			pyautogui.scroll(50)
		else:
			pyautogui.scroll(-50)

		
