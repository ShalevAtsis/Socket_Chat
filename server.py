import socket
from _thread import *
import threading

# Declare the host and port in which we want to communicate with clients
host = socket.gethostname() # Host is the server's machine hostname
port = 2025 # Port to listen on
clients = {} # Dictionary to store client names and their corresponding connections
shutdown_event = threading.Event() # Event to signal server shutdown
clients_lock = threading.Lock() # Lock to ensure thread safety when accessing clients dictionary

f = None
try:
    # Attempt to open the chat documentation file to store chat logs
    f = open("chat_documentation.txt", "w")
except IOError:
    print("Problem creating chat documentation file")

# Function to start the server and handle incoming connections
def start_server(host, port):
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind the socket to the host and port
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
        return

    print(f'Server is listing on the port {port}...')
    if f:
        f.write("Server is now alive and listening.\n")
    ServerSocket.listen() # Start listening for incoming connections

    # Start the accept_connection thread to handle incoming client connections
    start_new_thread(accept_connection, (ServerSocket,))

    while not shutdown_event.is_set():
        # Main thread checks for the shutdown command
        stop = input("Type 'Terminate server' to quit.\n")
        if stop == 'Terminate server':
            shutdown_server()

    # After server shutdown, write the shutdown message to the file
    if f:
        f.write("Server has been shutdown.\nChat finished.\n")
    ServerSocket.close() # Close the server socket
    close_file() # Close the chat documentation file

# Function to shut down the server gracefully
def shutdown_server():
    with clients_lock:
        for name, connection in list(clients.items()):
            try:
                # Notify each client that the server is shutting down
                connection.sendall(str.encode("\nServer is shutting down. Disconnecting...\n"))
                connection.close()  # Close the client connection
            except socket.error as e:
                print(f"Error disconnecting client {name}: {e}")
        clients.clear()  # Clear all client connections
    shutdown_event.set()  # Set the shutdown event to stop the server

# Function to register a new client after they connect
def register_client(connection):
    global f
    name = connection.recv(2048).decode('utf-8')  # Receive the client name
    with clients_lock:
        clients[name] = connection  # Store the client connection with their name
    connection.sendall(str.encode(f'Welcome {name}!\nUse "@<client_name> <message>" for private message.\nTo send to all, just type your message.\nTo disconnect, send "exit"\n'))
    if f:
        f.write(f"Client {name} has joined the chat room!\n")
    client_handler(connection, name)  # Start handling the client in a separate thread

# Function to handle the communication with each client
def client_handler(connection, sender_name):
    global f
    while True:
        try:
            # Receive data from the client
            data = connection.recv(2048)
            if not data:
                break  # Break if no data is received (client disconnected)
            message = data.decode('utf-8')

            # Log the message to the file
            if f:
                f.write(f"{sender_name}: {message}\n")

            # Handle client exit message
            if message == 'exit':
                broadcast_message(sender_name, f"has left the chat.")
                break
            # Handle private messages
            elif message.startswith('@'):
                target_name, msg = message[1:].split(' ', 1) # Extract target client and message
                send_to_client(sender_name, target_name, msg)
            else:
                # Broadcast to all clients if it's not a private message
                broadcast_message(sender_name, message)

        except socket.error as e:
            # Handle socket error (e.g., client disconnected unexpectedly)
            print(f"Error with client {sender_name}: {e}. Disconnecting.")
            break

    # Once client exits, close the connection and remove from the clients list
    print(f"Client {sender_name} disconnected.")
    if f:
        f.write(f"{sender_name} has been disconnected\n")
    del clients[sender_name]  # Remove client from dictionary
    connection.close()

# Function to send a private message to a specific client
def send_to_client(sender_name, target_name, message):
    with clients_lock:
        if target_name in clients:
            target_connection = clients[target_name]
            # Send private message to the target client
            target_connection.sendall(str.encode(f'Private message from {sender_name}: {message}'))
        else:
            # Notify sender if the target client is not found
            clients[sender_name].sendall(str.encode(f'Client "{target_name}" not found.'))

# Function to broadcast a message to all clients
def broadcast_message(sender_name, message):
    with clients_lock:
        for name, connection in list(clients.items()):
            if name != sender_name:  # Don't send the message back to the sender
                try:
                    connection.sendall(str.encode(f"{sender_name}: {message}"))
                except:
                    connection.close()  # Handle disconnection
                    del clients[name]

# Function to accept incoming client connections
def accept_connection(ServerSocket):
    while not shutdown_event.is_set():
        try:
            Client, address = ServerSocket.accept()
            print(f'Accepted connection from: {address[0]}:{str(address[1])}')
            start_new_thread(register_client, (Client,))  # Start a new thread to handle each client
        except socket.error as e:
            # Handle errors during client connection
            if shutdown_event.is_set():
                print("Server shutting down, no more connections accepted.")
            else:
                print(f"Error accepting connection: {e}")
            break

# Function to close the chat documentation file
def close_file():
    if f:
        f.close()

# Start the server
start_server(host, port)