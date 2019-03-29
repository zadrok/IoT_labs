from gpiozero import LED
from time import sleep

led1 = LED(2)
led2 = LED(3)
led3 = LED(4)

while True:
  led3.off()
  led1.on()
  sleep(1)
  led1.off()
  led2.on()
  sleep(1)
  led2.off()
  led3.on()
  sleep(1)
