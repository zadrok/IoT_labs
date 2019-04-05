from gpiozero import LED, Button
from time import sleep
import serial
port = "/dev/ttyACM0"

# open the serial port to talk over
s1 = serial.Serial(port,9600)
# clean the serial port
s1.flushInput()

# gpio ports led's and button is plugged into
led1 = LED(2)
led2 = LED(3)
led3 = LED(4)
button = Button(24)
#  what mode to be showing
flashMode = False

# what to do when the lights are inthe normal mode`
def normalTrafficLights():
  led3.off()
  led2.off()
  led1.on()
  sleep(1)
  led1.off()
  led2.on()
  sleep(1)
  led2.off()
  led3.on()
  sleep(1)

# what to do when in the flashing mode
def flashingTrafficLights():
  led1.off()
  led2.off()
  led3.off()
  sleep(1)
  led2.on()
  sleep(1)

# send data to Arduino over the serial
def signalToArduino(toSend):
  s1.write(toSend)

# receive data from the Arduino over the serial
def signalFromArduino():
  if s1.inWaiting() > 0:
    return True
  return False

# loop for order of operations
while True:
  # test button
  if button.is_pressed:
    # if button is pressed
    # change mode
    flashMode = not flashMode
    # send to Arduino
    signalToArduino(flashMode)

  # test if signal from arduino
  if signalFromArduino():
    # if true change mode
    flashMode = not flashMode

  # do one loop of the lights sequence
  if flashMode:
    flashingTrafficLights()
  else:
    normalTrafficLights()
