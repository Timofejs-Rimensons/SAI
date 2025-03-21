import json
import smbus
import RPi.GPIO as GPIO
import time
# 4096 steps per 360 degrees. Wait 1ms after each step

with open('const.json', 'r') as file:
    CONSTANTS = json.load(file)

step_motor_pins = (19,13,6,5)

GPIO.setup(step_motor_pins, GPIO.OUT)

def move_servo(angle: int):
    

dc_pwm1.stop()
GPIO.cleanup()