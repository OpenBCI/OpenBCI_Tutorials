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
time_thres = 2000
prev_time = 0
blink_thres = 0.95

while True:

	sample, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp

	curr_time = int(round(time.time() * 1000)) # get current time in milliseconds

	if ((sample[0] >=  blink_thres) & (curr_time - time_thres > prev_time)):  # if a blink is detected and enough time has gone by since the last blinking, press space
		prev_time = int(round(time.time() * 1000)) # update time 
		pyautogui.press('space')
		
