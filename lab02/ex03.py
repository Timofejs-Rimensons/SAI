from RPi import GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

leds = [10,9,11]

GPIO.setup(leds, GPIO.OUT)

led_num = len(leds)
state_changes = 0
while True:
    GPIO.output(leds, False)
    GPIO.output(leds[state_changes], True)
    state_changes = state_changes+1 if state_changes < led_num - 1 else 0
    sleep(0.5)

