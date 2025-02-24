import serial
import time
from includes import Gyems, CanBus

# Serial port configuration
SERIAL_PORT = "COM7"
BAUD_RATE = 115200
SQUEEZE_THRESHOLD = 120  # Adjust based on your EMG signal strength
HOLD_TIME_THRESHOLD = 0.5  # Holding duration threshold for rotation decision
EMG_ROTATE_THRESHOLD = 250  # Threshold for high EMG detected movement

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
time.sleep(2)  # Allow time for serial connection to stabilize

# Initialize CAN bus and motor
bus = CanBus()
motor = Gyems(bus)

# Enable the motor and set speed
motor.enable()
motor.set_angle(0, 1000)
time.sleep(1)

# Motor rotation logic
current_angle = 0
squeeze_start_time = None
holding = False
last_action_time = 0
original_position = 0  # To store the original position when holding
event_no = 0

print("Listening for EMG signals...")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()

            if "Filtered:" in line:
                try:
                    # Extract the filtered EMG value
                    filtered_value = int(line.split("Filtered:")[1].strip())
                    current_time = time.time()

                    if filtered_value > SQUEEZE_THRESHOLD:  
                        motor.set_angle(90, 500)
                    else:  # Release detected
                        motor.set_angle(0, 500)
            
                except ValueError:
                    pass  # Ignore any invalid data

    except KeyboardInterrupt:
        print("\nStopping motor and closing connection.")
        motor.disable()
        ser.close()
        break
