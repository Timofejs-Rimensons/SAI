import smbus
import RPi.GPIO as GPIO
import time

# GPIO Pin for Interrupt (INT)
INT_PIN = 8  # Connected to GPIO8

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use I2C bus 1 on Raspberry Pi

def scan_i2c():
    """Scans I2C bus and returns the detected sensor address."""
    print("Scanning for I2C devices...")
    for addr in range(0x03, 0x78):  # I2C address range
        try:
            bus.write_quick(addr)  # Check if a device responds
            print(f"Device found at 0x{addr:02X}")
            return addr
        except OSError:
            continue
    print("No I2C device found!")
    return None

# Detect sensor address
I2C_ADDRESS = scan_i2c()
if I2C_ADDRESS is None:
    exit("Exiting... No I2C device detected.")

# Setup GPIO for INT pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setup_max30102():
    """Configures MAX30102 with default settings."""
    try:
        # Reset the sensor
        bus.write_byte_data(I2C_ADDRESS, 0x09, 0x40)
        time.sleep(0.1)

        # Set SpO2 configuration (0x0A) – LED Pulse Width = 411μs, Sample Rate = 100Hz
        bus.write_byte_data(I2C_ADDRESS, 0x0A, 0x03)

        # Set Multi-LED Mode (0x0C) – Enable RED and IR LEDs
        bus.write_byte_data(I2C_ADDRESS, 0x0C, 0x03)

        print("MAX30102 initialized!")
    except Exception as e:
        print(f"Error initializing MAX30102: {e}")

def read_heart_rate():
    """Reads heart rate data from MAX30102 via I2C."""
    try:
        # Read IR value (16-bit) from FIFO register (0x07)
        data = bus.read_i2c_block_data(I2C_ADDRESS, 0x07, 6)  # FIFO Data Register
        ir_value = (data[0] << 16) | (data[1] << 8) | data[2]  # IR LED value
        red_value = (data[3] << 16) | (data[4] << 8) | data[5]  # RED LED value

        # Basic estimation: If IR value is high, assume heartbeat detected
        heart_rate = (ir_value // 1000) % 100  # Fake HR calculation, real HR needs processing

        return heart_rate, ir_value, red_value
    except Exception as e:
        print(f"Error reading heart rate: {e}")
        return None, None, None

def int_callback(channel):
    """Interrupt handler function, runs when INT pin goes LOW."""
    hr, ir, red = read_heart_rate()
    if hr is not None:
        print(f"Heart Rate: {hr} BPM | IR: {ir} | RED: {red}")

# Initialize the sensor
setup_max30102()

# Attach interrupt to INT pin
GPIO.add_event_detect(INT_PIN, GPIO.FALLING, callback=int_callback, bouncetime=200)

try:
    print(f"Monitoring heart rate... Sensor found at 0x{I2C_ADDRESS:02X}. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)  # Main loop does nothing, waits for interrupts

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
