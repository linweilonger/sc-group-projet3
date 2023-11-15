import socket
import csv
import glob
import json
import argparse
import os
from datetime import datetime, timedelta

def connect_to_peer(host, port):
    """Establish a connection to the peer server."""
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((host, port))
        return peer_socket
    except socket.error as e:
        print(f"Connection error: {e}")
        return None

def disconnect_from_peer(peer_socket):
    """Disconnect from the peer server."""
    peer_socket.close()

def read_csv_file(filepath):
    """Read data from a CSV file and return it as a dictionary."""
    data = []
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        sublists = [[] for _ in headers]
        for row in csv_reader:
            for i in range(len(headers)):
                sublists[i].append(row[i])

        data_dict = {}
        for i in range(len(headers)):
            data_dict[headers[i]] = sublists[i]
    return data_dict

def send_peer_data(peer_socket, peer_id, filename, data_dict):
    """Send data to the peer server."""
    try:
        message = f"{peer_id}:{filename.split('.csv')[0]}:{json.dumps(data_dict)}"
        peer_socket.send(message.encode('utf-8'))

        # Wait for a response if needed
        response = peer_socket.recv(90000)
        print(f"Peer response: {response.decode('utf-8')}")

    except socket.error as e:
        print(f"Socket error: {e}")

def main(peer_ips, port, peer_id):
    """Main function to connect to the peer and send data."""
    try:
        current_datetime = datetime.now()
        previous_datetime = current_datetime - timedelta(hours=1)
        current_date = previous_datetime.strftime("%Y-%m-%d")
        current_hour = previous_datetime.strftime("%H")

        csv_files = glob.glob(os.path.join("/users/pgrad/singhr6/group24/data", current_date, current_hour, "*.csv"))

        if csv_files:
            for csv_file in csv_files:
                for peer_ip in peer_ips:
                    # Connect to the peer server for each file
                    peer_socket = connect_to_peer(peer_ip, port)
                    if peer_socket:
                        filename = csv_file.split('/')[-1]
                        data = read_csv_file(csv_file)
                        send_peer_data(peer_socket, peer_id, filename, data)

                        # Disconnect from the peer server after each file
                        disconnect_from_peer(peer_socket)
                        break  # Move to the next file after successfully sending to a peer
        else:
            print("No CSV files found for Date: " + current_date + " Hour: " + current_hour)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send data to a peer.")
    parser.add_argument("--peer_ips", nargs='+', default=['10.35.70.28', '10.35.70.42', '10.35.70.31'], help="List of peer IP addresses")
    parser.add_argument("--port", type=int, default=33334, help="Port number")
    parser.add_argument("--peer_id", default='Curiosity_Rover', help="Unique identifier for this peer")
    args = parser.parse_args()

    main(args.peer_ips, args.port, args.peer_id)

