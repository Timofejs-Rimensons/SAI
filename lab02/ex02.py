from RPi import GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

leds = [9,10,11]
btns = [20,21]

GPIO.setup(btns, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(leds, GPIO.OUT)

led_num = len(leds)
state_changes = 0
timer_start = 0
last_btn1_state = False
last_btn2_state = False
next_led_state = True
ready_to_change = True
while True:
    btn1_state = GPIO.input(btns[0])
    btn2_state = GPIO.input(btns[1])
    if last_btn1_state != btn1_state:
        if not btn1_state:
            if state_changes == led_num:
                GPIO.output(leds, False)
                state_changes = 0
            else:
                GPIO.output(leds, False)
                GPIO.output(leds[state_changes], True)
                state_changes += 1


    if not btn2_state:
        if ready_to_change:
            if timer_start == 0:
                timer_start = int(time.time())
            elif int(time.time()) - timer_start >= 2:
                timer_start = 0
                state_changes = 0
                
                GPIO.output(leds, next_led_state)
                next_led_state = not next_led_state
                ready_to_change = False
    else:
        timer_start = 0
        ready_to_change = True


    sleep(0.1)

    last_btn1_state = btn1_state
    last_btn2_state = btn2_state