import serial
import csv
import time
from includes import Gyems, CanBus

def compute_control_with_integral(target_force, current_angle, current_speed, kp, kd, ki, integral):
    position_error = target_force - current_angle
    speed_error = 0 - current_speed  # Target speed is 0 when resisting force
    integral += position_error  # Accumulate integral term
    return kp * position_error + kd * speed_error + ki * integral, integral

def compute_control(target_force, current_angle, current_speed, kp, kd):
    position_error = target_force - current_angle
    speed_error = 0 - current_speed  # Target speed is 0 when resisting force
    return kp * position_error + kd * speed_error

# Initialize serial connection for force sensor
sensor_serial = serial.Serial('COM7', 115200, timeout=1)

# Initialize CAN bus and motor. Thanks to the "includes"
bus = CanBus()
motor = Gyems(bus)

# Control parameters for stronger resistance and smoother return
kp, kd, ki = 10, 3, 0.2
integral_term = 0

target_position = 0  # Original position


# CSV Logging Setup
csv_filename = "motor_force_data.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Motor Angle", "Force (g)", "Torque (Nm)"])  # Column headers

    try:
        motor.enable()
        motor.set_zero()
        start_time = time.time()
        
        while True:
            if sensor_serial.in_waiting > 0:
                raw_data = sensor_serial.readline().decode('utf-8').strip()
                try:
                    force_value = float(raw_data)
                except ValueError:
                    continue  # Ignore invalid sensor data
                
                motor_status = motor.info()
                current_angle = motor_status['angle']
                current_speed = motor_status['speed']
                current_torque = motor_status['torque']  # torque instead of "current"

                # control_signal, integral_term = compute_control_with_integral(-force_value/10, motor_status['angle'], motor_status['speed'], kp, kd, ki, integral_term)
                control_signal= compute_control(-force_value, motor_status['angle'], motor_status['speed'], kp, kd)
                motor.set_speed(control_signal)
                
                # Return smoothly when force is released
                if force_value < 1:  # Small threshold to detect release
                    # return_signal, integral_term = compute_control_with_integral(target_position, motor_status['angle'], motor_status['speed'], kp, kd, ki, integral_term)
                    return_signal = compute_control(target_position, motor_status['angle'], motor_status['speed'], kp, kd)
                    motor.set_speed(return_signal)
                
                # Log data to CSV
                elapsed_time = time.time() - start_time
                writer.writerow([elapsed_time, current_angle, force_value, current_torque])

                # print(f"Force: {force_value}, Motor Angle: {motor_status['angle']}, Applied Speed: {control_signal}")
                print(f"Time: {elapsed_time:.2f}s | Force: {force_value}g | Angle: {current_angle:.2f}° | Torque: {current_torque:.2f} Nm")


    except KeyboardInterrupt:
        print("\nStopping program...")


    finally:
        print("Disabling motor and closing connections...")
        motor.disable(True)
        sensor_serial.close()
        if hasattr(bus, "close"):
            bus.close()