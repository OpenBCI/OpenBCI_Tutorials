# Code written by Rakesh C Jakati for the Motor Imagery tutorial

from oscpy.server import OSCThreadServer
from time import sleep
from oscpy.client import OSCClient

osc = OSCThreadServer()
sock = osc.listen(address='127.0.0.1', port=9002, default=True)
@osc.address(b'/neuropype')
def callback(left, right):
  print("Left prediction : ",round(left,2),"Right prediction : ",round(right,2))
sleep(100)

