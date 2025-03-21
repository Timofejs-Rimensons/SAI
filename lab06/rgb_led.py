import smbus
import RPi.GPIO as GPIO
import time

RED_PIN = 5
GREEN_PIN = 6
BLUE_PIN = 13
BUTTON_PIN = 20

POT_R = 0
POT_G = 1
POT_B = 2

I2C_ADDRESS = 0x48

bus = smbus.SMBus(1)

system_on = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

pwm_r = GPIO.PWM(RED_PIN, 1000)
pwm_g = GPIO.PWM(GREEN_PIN, 1000)
pwm_b = GPIO.PWM(BLUE_PIN, 1000)

pwm_r.start(100)
pwm_g.start(100)
pwm_b.start(100)

def read_adc(channel):
    command = 0x84 | ((channel & 0x07) << 4)
    bus.write_byte(I2C_ADDRESS, command)
    return bus.read_byte(I2C_ADDRESS)

def toggle_system(channel):
    global system_on
    system_on = not system_on
    print(f"System {'ON' if system_on else 'OFF'}")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=toggle_system, bouncetime=300)



try:
    while True:
        if system_on:
            r_val = read_adc(POT_R) / 255 * 100
            g_val = read_adc(POT_G) / 255 * 100
            b_val = read_adc(POT_B) / 255 * 100

            pwm_r.ChangeDutyCycle(100 - r_val)  
            pwm_g.ChangeDutyCycle(100 - g_val)
            pwm_b.ChangeDutyCycle(100 - b_val)
            print(f"R: {r_val}, G: {g_val}, B: {b_val}")
        else:
            pwm_r.ChangeDutyCycle(100-1e-10)  
            pwm_g.ChangeDutyCycle(100-1e-10)
            pwm_b.ChangeDutyCycle(100-1e-10)

        time.sleep(0.1)

except KeyboardInterrupt:
    pwm_r.stop()
    pwm_g.stop()
    pwm_b.stop()
    GPIO.cleanup()
