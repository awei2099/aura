import socket as s
import io
import json
import base64
from AI import Chatbot
import threading as t
import os
import subprocess
import miniupnpc
import signal
import atexit

APIKEY = open("apikey openai.txt", "r+").read()

# Create a UPnP object and discover devices
upnp = miniupnpc.UPnP()
upnp.discoverdelay = 2000

try:
    ndevices = upnp.discover()
    print(f"Number of UPnP devices discovered: {ndevices}")
    upnp.selectigd()
except Exception as e:
    print(f"UPnP discovery failed: {e}")
    exit(1)

HOST = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()  # Windows: s.gethostbyname(s.gethostname())
PORT = 7106
MAX_BYTES_ACCEPTED = 4096 * 8

try:
    # Request port forwarding
    external_ip = upnp.externalipaddress()
    print(f"External IP address: {external_ip}")
    upnp.addportmapping(PORT, 'TCP', HOST, PORT, 'My Server', '')
    print(f"Port {PORT} forwarding to {HOST} enabled.")
except Exception as e:
    print(f"Failed to add port mapping: {e}")
    exit(1)

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(100)

def handle_client(communication_socket, ai):
    print("Running handle")
    data = receive_data(communication_socket)
    data = json.loads(data)

    sysMessage = data.get('sys')
    question = data.get('question')
    image_data = data.get('image')

    print(f"Message from client: {sysMessage}")
    if sysMessage == "Quit":
        communication_socket.close()
        print("Stopping handle...")
    else:
        if sysMessage == "Convo":
            list = ai.getConvo()
            data = {}
            for i in range(len(list)):
                data[i] = list[i]
            data = json.dumps(data).encode('utf-8')
            communication_socket.send(data)
        elif image_data:
            image = base64.b64decode(image_data)
            with open("Temp/received_image" + str(count("Temp")) + ".jpg", "wb") as f:
                f.write(image)
            print("Image received.")
            communication_socket.send(ai.questionImage(question, image_data).encode('utf-8'))
        else:
            communication_socket.send(ai.question(question).encode('utf-8'))
        handle_client(communication_socket, ai)

def count(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def receive_data(sock):
    # First, read the length of the JSON data (4 bytes)
    data_length = int.from_bytes(sock.recv(4), 'big')
    
    # Now, read the actual JSON data
    data = b''
    while len(data) < data_length:
        part = sock.recv(min(data_length - len(data), MAX_BYTES_ACCEPTED))
        data += part
    return data.decode('utf-8')

# Cleanup function to remove port mapping
def cleanup():
    try:
        upnp.deleteportmapping(PORT, 'TCP')
        print("Port mapping removed.")
    except Exception as e:
        print(f"Failed to remove port mapping: {e}")

# Register the cleanup function to run on normal program exit
atexit.register(cleanup)

# Handle termination signals to ensure cleanup is run
def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    cleanup()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("Starting Server")
while True:
    print("Listening for new connection")
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    t.Thread(target=handle_client, args=[communication_socket, Chatbot(APIKEY)]).start()
