from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ledPin = 17
btnPin = 20

GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)

ledState = False
lastBtnState = False
while True:
    if lastBtnState != GPIO.input(btnPin):
        sleep(0.05)
        ledState = not ledState
        GPIO.output(ledPin, ledState)
        print(ledState)
        while not GPIO.input(btnPin):
            sleep(0.1)
    lastBtnState = GPIO.input(btnPin)