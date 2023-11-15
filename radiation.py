import random
import time
import csv
import os
from datetime import datetime


def collect_radiation_data():
    LOW = 0.1
    HIGH = 0.4
    radiation_level = random.uniform(LOW, HIGH)
    #print(f"radiation_level: {radiation_level} μSv/h")
    return radiation_level

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_radiation_data(directory_to_write, timestamp, radiation, data_unit):
    # Use the provided path and append folder and file name
    cloud_docs_path = 'radiation.csv'
    file_path = os.path.join(directory_to_write, cloud_docs_path)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty, and if so, write the header
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", f"radiation_level({data_unit})"])

        writer.writerow([timestamp, radiation])


# Set the duration for the script to run (24 hours)
duration = 24 * 60 * 60  # 24 hours in seconds
start_time = time.time()
radiation_unit = "μSv/h"

while True:
    # Check if 24 hours have passed
    if time.time() - start_time > duration:
        break

    # radiation reading
    radiation = collect_radiation_data()

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Create directories for each day and hour
    day_directory = current_timestamp.strftime("%Y-%m-%d")
    hour_directory = current_timestamp.strftime("%H")
    directory_to_write = os.path.join("data", day_directory, hour_directory)
    create_directory_if_not_exists("data")
    create_directory_if_not_exists(os.path.join("data", day_directory))
    create_directory_if_not_exists(directory_to_write)
    
    # Save the radiation reading with timestamp to the CSV file
    save_radiation_data(directory_to_write, current_timestamp, radiation, radiation_unit)

    # Print the simulated radiation reading with timestamp (optional)
    print(f"{current_timestamp} - radiation: {radiation} {radiation_unit}")

    # Wait for 5 seconds before generating the next reading
    time.sleep(5)

# Print a message indicating the end of the script
print("Script completed after 5 minutes.")

