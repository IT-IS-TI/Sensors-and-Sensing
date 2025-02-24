import serial
import time
from includes import Gyems, CanBus

# Serial port configuration
SERIAL_PORT = "COM7"
BAUD_RATE = 115200
SQUEEZE_THRESHOLD = 120  # Adjust based on your EMG signal strength
HOLD_TIME_THRESHOLD = 0.5  # Holding duration threshold for rotation decision

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
time.sleep(2)  # Allow time for serial connection to stabilize

# Initialize CAN bus and motor
bus = CanBus()
motor = Gyems(bus)

# Enable the motor and set speed
motor.enable()
motor.set_angle(0, 1000)
time.sleep(2)

# Motor rotation logic
current_angle = 0
squeeze_start_time = None
holding = False
last_action_time = 0
original_position = 0  # To store the original position when holding
event_no = 0

def rotate_motor(degrees):
    """Rotates the motor by the given degrees."""
    global current_angle
    target_angle = current_angle + degrees
    motor.set_angle(target_angle, 500)
    current_angle = target_angle  # Update the current position
    print(f"Rotated to {current_angle}°")

print("Listening for EMG signals...")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8", errors="replace").strip()

            if "Filtered:" in line:
                try:
                    # Extract the filtered EMG value
                    filtered_value = int(line.split("Filtered:")[1].strip())
                    current_time = time.time()

                    if filtered_value > SQUEEZE_THRESHOLD:  
                        if squeeze_start_time is None:  # Squeeze detected
                            squeeze_start_time = current_time
                            holding = False  # Reset holding flag
                    else:  # Release detected
                            if squeeze_start_time is not None:
                                squeeze_duration = current_time - squeeze_start_time

                                if squeeze_duration < HOLD_TIME_THRESHOLD:
                                    event_no += 1
                                    print(event_no)
                                    print("Quick squeeze detected! Rotating 90°")
                                    rotate_motor(90)
                                else:
                                    event_no += 1
                                    print(event_no)
                                    print("Holding detected! Rotating -90°")
                                    original_position = current_angle  # Save position
                                    rotate_motor(-90)
                                    holding = True  # Mark that we're holding

                                squeeze_start_time = None  # Reset timer

                except ValueError:
                    pass  # Ignore any invalid data

    except KeyboardInterrupt:
        print("\nStopping motor and closing connection.")
        motor.disable()
        ser.close()
        break
