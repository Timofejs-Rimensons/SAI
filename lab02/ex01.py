from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ledPin = 17
btns = [20,21,16,26]

GPIO.setup(btns, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)

led_state = False
last_btn1_state = True
GPIO.output(ledPin, False)
while True:
    sleep(0.1)
    btn0_state = GPIO.input(btns[0])
    btn1_state = GPIO.input(btns[1])
    btn2_state = GPIO.input(btns[2])
    btn3_state = GPIO.input(btns[3])

    if last_btn1_state != btn1_state:
        last_btn1_state = btn1_state
        if not btn1_state:
            GPIO.output(ledPin, False)
            led_state = False
            continue
        else:
            GPIO.output(ledPin, True)
            led_state = True

    if not btn0_state:
        GPIO.output(ledPin, True)
        led_state = True

    if not btn3_state:
        led_state = not led_state
        GPIO.output(ledPin, led_state)
        sleep(2)

    if not btn2_state:
        led_state = not led_state
        GPIO.output(ledPin, led_state)
        sleep(0.5)
    

