import json
import RPi.GPIO as GPIO
import time

with open('const.json', 'r') as file:
    CONSTANTS = json.load(file)

servo_pin = 18

GPIO.setup(servo_pin, GPIO.OUT)

def move_servo(angle: int):


dc_pwm1.stop()
GPIO.cleanup()