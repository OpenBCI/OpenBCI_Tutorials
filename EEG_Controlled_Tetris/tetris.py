import socket
import sys
import time
import argparse
import signal
import json
import pyautogui

"""Code modified from the example program to show how to read a multi-channel time series from UDP at https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/UDP/udp_receive.py."""

""" These variables can be changed if needed for changed controls on different Tetris websites. Refer to pyautogui documentation for 
more information on what keywords map to specific keys. https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys """

MOVE_PIECE_LEFT = "left"
MOVE_PIECE_RIGHT = "right"
DROP_PIECE = "space"
ROTATE_PIECE = "up"


# Clean exit from print mode
def exit_print(signal, frame):
    print("Closing listener")
    sys.exit(0)


if __name__ == "__main__":
    # Collect command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=12345, help="The port to listen on")
    parser.add_argument("--address", default="/openbci", help="address to listen to")
    parser.add_argument("--option", default="print", help="Debugger option")
    parser.add_argument("--len", default=8, help="Debugger option")
    args = parser.parse_args()

    # Set up necessary parameters from command line
    length = args.len
    if args.option == "print":
        signal.signal(signal.SIGINT, exit_print)

    # Connect to socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (args.ip, args.port)
    sock.bind(server_address)

    # Display socket attributes
    print('--------------------')
    print("-- UDP LISTENER -- ")
    print('--------------------')
    print("IP:", args.ip)
    print("PORT:", args.port)
    print('--------------------')

    # Receive messages
    print("Calibration period, remain neutral...")
    start = time.time()
    numSamples = 0
    duration = 10
    rotated = False
    space_pressed = False
    left_once = False
    right_once = False
    x_prev = 0
    z_prev = 0

    x_start_sum = 0
    x_start_samples = 0
    for y in range(150):
        data, addr = sock.recvfrom(20000)  # buffer size is 20000 bytes
        obj = json.loads(data.decode())
        if obj.get('type') == 'accelerometer':
            aux_data = obj.get('data')
            x_start_sum += aux_data[0]
            x_start_samples += 1

    print("Calibration done. You may now begin Tetris!")

    x_start = x_start_sum / x_start_samples

    while True:
        data, addr = sock.recvfrom(20000)  # buffer size is 20000 bytes
        if args.option == "print":
            obj = json.loads(data.decode())
            if obj.get('type') == 'accelerometer':
                aux_data = obj.get('data')
                x = aux_data[0]
                z = aux_data[2]
                if z > 0.5 and z_prev < z and not space_pressed:  # drop piece
                    pyautogui.press('space')
                    space_pressed = True
                else:
                    if 0.075 + x_start < x < 0.2 + x_start and not left_once:  # short left
                        pyautogui.press('left')
                        left_once = True
                        space_pressed = False
                    elif -0.075 + x_start > x > -0.2 + x_start and not right_once:  # short right
                        pyautogui.press('right')
                        right_once = True
                        space_pressed = False
                    elif x > 0.2 + x_start and x_prev < x:  # move left
                        pyautogui.press('left')
                        left_once = False
                        space_pressed = False
                    elif x < -0.2 + x_start and x_prev > x:  # move right
                        pyautogui.press('right')
                        right_once = False
                        space_pressed = False
                    elif -0.075 + x_start < x < 0.075 + x_start:  # head is neutral
                        left_once = False
                        right_once = False
                        space_pressed = False
                    elif z < 0.5:
                        space_pressed = False
                if z > 0.5:
                    space_pressed = True
                x_prev = x
                z_prev = z
            else:
                emg_data = obj.get('data')
                fp1 = emg_data[0]
                fp2 = emg_data[1]
                to_continue = 0
                for i in range(2, 8):
                    if emg_data[i] > 0.8:
                        to_continue += 1
                if (to_continue < 4):
                    if fp2 < 0.9:
                        rotated = False
                    elif (fp2 > 0.9) and not rotated:
                        pyautogui.press('up')
                        rotated = True
            numSamples += 1
