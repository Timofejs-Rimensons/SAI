import RPi.GPIO as GPIO
import numpy as np
import smbus
import json
import time

class IORepo():

    def __init__(self):

        with open('const.json', 'r') as file:
            self.CONSTANTS = json.load(file)
        
        # Servo_motor
        self.dc_for_0 = self.CONSTANTS["servo_motor"]["0_degrees"]
        self.dc_for_180 = self.CONSTANTS["servo_motor"]["180_degrees"]


    def servo_motor(self, servopin: int, degree: int) -> None:
        servo_pwm = GPIO.PWM(servopin, 50)
        if degree == 0:
            duty_cycle = self.dc_for_0 * 5
        elif degree >= 180:
            duty_cycle = self.dc_for_180 * 5
        else:
            duty_cycle = degree / 36
        
        servo_pwm.start()
