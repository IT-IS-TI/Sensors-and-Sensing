import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_filename = "motor_force_data.csv"
df = pd.read_csv(csv_filename)

# Extract columns
time_data = df["Time (s)"]
angle_data = df["Motor Angle"]
force_data = df["Force (g)"]
torque_data = df["Torque (Nm)"]

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 10))

# Force vs. Motor Angle
axs[0].plot(angle_data, force_data, 'bo-')
axs[0].set_title("Force vs. Motor Angle")
axs[0].set_xlabel("Motor Angle (°)")
axs[0].set_ylabel("Force (g)")

# Force vs. Motor Torque
axs[1].plot(force_data, torque_data, 'ro-')
axs[1].set_title("Force vs. Motor Torque")
axs[1].set_xlabel("Force (g)")
axs[1].set_ylabel("Torque (Nm)")

# Motor Angle over Time
axs[2].plot(time_data, angle_data, 'g-')
axs[2].set_title("Motor Angle over Time")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Motor Angle (°)")

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig("motor_plot.jpg")
plt.show()
