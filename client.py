import socket
import threading
import sys

# Prompt the user for their name
client_name = input("Hello client.\nPlease enter your name: ")

# Define the host and port for connecting to the server
host = socket.gethostname()  # or use the server's IP address
port = 2025

# Event object to handle server disconnection and stop threads
disconnect_event = threading.Event()

# Function to receive messages from the server in a separate thread
def receive_messages(client_socket):
    while not disconnect_event.is_set():
        try:
            # Try to receive the message from the server
            message = client_socket.recv(2048).decode('utf-8')

            # If no message is received, the server may have closed the connection
            if not message:
                print("Server closed the connection.")
                disconnect_event.set()  # Signal disconnection
                break
            # Print the received message
            print(message)
        except socket.error as e:
            # Handle socket error (e.g., connection issues)
            print(f"Error receiving message: {e}")
            disconnect_event.set()  # Signal disconnection
            break
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error: {e}")
            disconnect_event.set()  # Signal disconnection
            break

    # After the loop ends, close the socket and exit
    print("Exiting receive thread...")
    client_socket.close()
    sys.exit(0)  # Ensure the client process exits when server disconnects

# Main function for connecting to the server and handling user input
def main():
    # Create a socket object to connect to the server
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    print("Connecting to server...")
    try:
        # Connect to the server using the specified host and port
        ClientSocket.connect((host, port))
        # Send the client's name to the server upon connection
        ClientSocket.send(str.encode(client_name))

        # Start a separate thread to handle receiving messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(ClientSocket,))
        receive_thread.start()

        # Main loop for sending messages from the client to the server
        while not disconnect_event.is_set():  # Main thread checks for disconnection
            try:
                # Prompt the user for input
                message = input()

                # If the server has disconnected, stop further input
                if disconnect_event.is_set():
                    break

                # If the user types 'exit', disconnect from the server
                if message == 'exit':
                    print("You have disconnected from the server.")
                    ClientSocket.send(str.encode(f"{client_name} has left the chat."))
                    break

                # Otherwise, send the user's message to the server
                ClientSocket.send(str.encode(message))

            except socket.error as e:
                # Handle any socket error during message sending
                print(f"Error sending message: {e}")
                disconnect_event.set() # Signal disconnection
                break
            except EOFError:  # Catch CTRL+D/EOF (end of file) to stop input
                print("EOF encountered. Exiting.")
                disconnect_event.set() # Signal disconnection
                break

    except socket.error as e:
        # Handle any connection-related errors (e.g., server unavailable)
        print(f"Connection error: {e}")

    finally:
        # Ensure the receiver thread stops when client is closing
        disconnect_event.set()
        # Close the socket connection
        ClientSocket.close()
        print("\nConnection closed.")
        # Exit the client process
        sys.exit(0)  # Terminate the client process

main()