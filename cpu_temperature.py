import random
import time
import csv
import os
from datetime import datetime

def collect_cpu_temperature_data():
    cpu_temperature = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    cpu_temperature = float(cpu_temperature) / 1000.00
    return cpu_temperature

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_cpu_temperature_data(directory, timestamp, temperature, data_unit):
    file_name = "cpu_temperature.csv"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", f"CPU Temperature({data_unit})"])
        writer.writerow([timestamp, temperature])

# Set the duration for the script to run (24 hours)
duration = 24 * 60 * 60  # 24 hours in seconds
start_time = time.time()
cpu_temperature_unit = "°C"

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

    # CPU temperature reading
    temperature = collect_cpu_temperature_data()

    # Save the temperature reading with timestamp to the CSV file
    save_cpu_temperature_data(directory_to_write, current_timestamp, temperature, cpu_temperature_unit)

    # Print the temperature reading with timestamp (optional)
    print(f"{current_timestamp} - CPU Temperature: {temperature} {cpu_temperature_unit}")

    # Wait for 5 seconds before generating the next reading
    time.sleep(5)

# Print a message indicating the end of the script
print("Script completed after 24 hours.")

