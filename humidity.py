import random
import time
import csv
import os
from datetime import datetime

def simulate_humidity():
    min_humidity = 10.0
    max_humidity = 40.0
    humidity = random.uniform(min_humidity, max_humidity)
    return humidity

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_humidity_data(directory, timestamp, humidity):
    file_name = "humidity.csv"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", "Humidity"])
        writer.writerow([timestamp, humidity])

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

    # Generate simulated humidity reading
    humidity = simulate_humidity()

    # Save the simulated humidity reading with timestamp to the CSV file
    save_humidity_data(directory_to_write, current_timestamp, humidity)

    # Print the simulated humidity reading with timestamp (optional)
    print(f"{current_timestamp} - Simulated Humidity: {humidity}%")

    # Wait for 5 seconds before generating the next reading
    time.sleep(5)

# Print a message indicating the end of the script
print("Script completed after 24 hours.")

