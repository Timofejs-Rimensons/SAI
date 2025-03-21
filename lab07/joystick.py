import smbus
import RPi.GPIO as GPIO
import time
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

BUZZER_P = 4
JOYSTICK_BTN = 7

BTN_0 = 16
BTN_1 = 20
BTN_2 = 21
BTN_3 = 26

JOYSTICK_X = 3
JOYSTICK_Y = 4

POSITIONS = {  # C-centre, L-left, R-right, U-up, D-down
    "CC": np.array([126, 137]),
    "LC": np.array([126, 134]),
    "RC": np.array([126, 141]),
    "CU": np.array([253, 68]),
    "CD": np.array([0, 145]),
    "LU": np.array([253, 171]),
    "LD": np.array([0, 177]),
    "RU": np.array([253, 61]),
    "RD": np.array([0, 84]),
}

I2C_ADDRESS = 0x48
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_P, GPIO.OUT)

for btn in [BTN_0,BTN_1, BTN_2, BTN_3, JOYSTICK_BTN]:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buzz(buzzerPin: int, freq: int, delay: float):
    pwm = GPIO.PWM(buzzerPin, freq)

    pwm.start(5)

    time.sleep(delay)

    pwm.stop()

def read_adc(channel):
    command = 0x84 | ((channel & 0x07) << 4)
    bus.write_byte(I2C_ADDRESS, command)
    return bus.read_byte(I2C_ADDRESS)

def current_pos(new_cords: np.array):
    print(new_cords)
    for key, pos in POSITIONS.items():
        if np.all((new_cords >= pos * 0.7) & (new_cords <= pos * 1.3)):

            return key
    return "ND" # Not detected


def plot_points(points: list[np.ndarray], filename="plot.png"):
    points = np.array(points)  
    plt.scatter(points[:, 0], points[:, 1], color="blue", marker="o", label="Pos")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Pos")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename, dpi=300, bbox_inches="tight")  # Save as PNG
    plt.close()


def main():
    dot_list = []
    timestamp_start = dt.now().timestamp()
    try: #
        while True:
            time.sleep(0.001)
            y_val = read_adc(JOYSTICK_Y) / 255 * 100
            x_val = read_adc(JOYSTICK_X)
            dot_list.append(np.array([x_val, y_val]))
            timestamp_now = dt.now().timestamp()
            print(timestamp_now - timestamp_start)
            if timestamp_now - timestamp_start >= 10:
                break

        plot_points(dot_list)

    except Exception as e:
        print(e)
        print("Stopping...")

main()