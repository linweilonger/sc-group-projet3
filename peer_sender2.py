import socket
import csv
import glob
import json
import argparse
import os

def connect_to_peer(host, port):
    """Establish a connection to the peer server."""
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((host, port))
        return peer_socket
    except socket.error as e:
        print(f"Connection error: {e}")
        return None


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
    message = f"{peer_id}:{filename.split('.csv')[0]}:{json.dumps(data_dict)}"
    peer_socket.send(message.encode('utf-8'))


def main(peer_ip, port, peer_id):
    """Main function to connect to the peer and send data."""
    peer_socket = connect_to_peer(peer_ip, port)
    if peer_socket is None:
        print("Could not connect to peer. Exiting.")
        return

    try:
        csv_files = glob.glob(os.path.join("*/*/*/*.csv"))
        for csv_file in csv_files:
            filename = csv_file.split('/')[-1]
            data = read_csv_file(csv_file)
            send_peer_data(peer_socket, peer_id, filename, data)

        response = peer_socket.recv(1024)
        print(f"Peer response: {response.decode('utf-8')}")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        peer_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send data to a peer.")
    parser.add_argument("--peer_ip", default='10.35.70.31', help="Peer's IP address")
    parser.add_argument("--port", type=int, default=33334, help="Port number")
    parser.add_argument("--peer_id", default='Curiosity_Rover', help="Unique identifier for this peer")
    args = parser.parse_args()

    main(args.peer_ip, args.port, args.peer_id)

