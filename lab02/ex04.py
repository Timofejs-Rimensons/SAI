import RPi.GPIO as GPIO
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


BUTTON_PIN = 20 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CSV_FILE = "data/btn_timings.csv"
os.makedirs("data", exist_ok=True)

def log_button_press():
    print("Waiting for button press...")
    while True:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        start_time = time.time()
        print("Button pressed...")

        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        end_time = time.time()
        duration = round(end_time - start_time, 3)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Button released! It was {duration} seconds")
        
        new_data = pd.DataFrame([[timestamp, duration]], columns=["Timestamp", "Duration (seconds)"])
        
        if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
            new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            new_data.to_csv(CSV_FILE, mode='w', header=True, index=False)




if __name__ == "__main__":
    log_button_press()

