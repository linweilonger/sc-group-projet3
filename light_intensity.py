import random
import time
import csv
import os
from datetime import datetime

def simulate_light_intensity():
    light_intensity = random.uniform(0, 100)  # Adjust the range as needed
    return light_intensity

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_light_data(directory, timestamp, light_intensity):
    file_name = "light_intensity.csv"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", "Light Intensity (lux)"])
        writer.writerow([timestamp, light_intensity])

# Set the duration for the script to run (24 hours)
duration = 24 * 60 * 60  # 24 hours in seconds
start_time = time.time()

while True:
    # Check if 24 hours have passed
    if time.time() - start_time > duration:
        break

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Create directories for each day and hour
    day_directory = current_timestamp.strftime("%Y-%m-%d")
    hour_directory = current_timestamp.strftime("%H")
    directory_to_write = os.path.join("data", day_directory, hour_directory)
    create_directory_if_not_exists("data")
    create_directory_if_not_exists(os.path.join("data", day_directory))
    create_directory_if_not_exists(directory_to_write)

    # Generate simulated light intensity reading
    light_intensity = simulate_light_intensity()

    # Save the simulated light intensity reading with timestamp to the CSV file
    save_light_data(directory_to_write, current_timestamp, light_intensity)

    # Print the simulated light intensity reading with timestamp (optional)
    print(f"{current_timestamp} - Simulated Light Intensity: {light_intensity} lux")

    # Wait for 5 seconds before generating the next reading
    time.sleep(5)

# Print a message indicating the end of the script
print("Script completed after 24 hours.")

