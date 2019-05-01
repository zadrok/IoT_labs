import serial
from random import randint
import time

port = "/dev/ttyACM0"

# open the serial port to talk over
s1 = serial.Serial(port,9600)
# clean the serial port
s1.flushInput()


while(True):

  if s1.inWaiting():
    result = str( s1.readline() )[2:-5]
    print( 'serial string: ' + result )
  else:
    print( 'nothing waiting' )

  s1.write( randint(1, 100) )

  time.sleep(1)
