# Socket_Chat

A multithreaded chat server implemented in Python using TCP sockets. Supports real-time communication between multiple clients with both private and broadcast messaging, session logging, and graceful shutdown. Includes both script and executable versions for ease of use.

## Features

- **Multithreaded Server**: Each client connection is handled in a separate thread.
- **Private and Broadcast Messaging**: Send direct messages or messages to all connected clients.
- **Graceful Shutdown**: Clients and the server can disconnect cleanly using dedicated commands.
- **Chat Logging**: All messages are recorded in `chat_documentation.txt`.
- **Cross-Platform Execution**: Run via Python scripts or provided executables.

## File Structure

- `server.py` / `server.exe` – Server implementation in script and executable form.
- `client.py` / `client.exe` – Client implementation in script and executable form.
- `chat_documentation.txt` – Generated chat session log.
- `Multi-Threaded Chat Server.pdf` – Full documentation and setup guide.

## How to Run

### Method 1: Executables

1. Run `server.exe`. Type `Terminate server` in the console to stop.
2. Run `client.exe` for each client instance. Enter a unique name when prompted.
3. Use `@client_name message` to send private messages.
4. Type `exit` to disconnect a client.

> **Note**: If your firewall or antivirus blocks the executables, either allow them explicitly or use the Python scripts instead.

### Method 2: Python Scripts

1. Open the project folder in your IDE.
2. Run `server.py` to start the server.
3. Duplicate `client.py` as `client_1.py`, `client_2.py`, etc. for multiple clients.
4. Run each client script in a separate terminal or IDE instance.
5. Use the same messaging and exit commands as in Method 1.

## Usage Example

- **Broadcast**: Type a message and press Enter.
- **Private Message**: `@username Hello there`
- **Disconnect Client**: Type `exit`
- **Shutdown Server**: Type `Terminate server`

## Requirements

- Python 3.x (if using scripts)
- Compatible OS for running `.exe` files (Windows)

## Author

**Shalev Atsis**  
Computer Science Student, HIT College  
📞 +972-58-5060699  
📧 [Shalevatsis@gmail.com](mailto:Shalevatsis@gmail.com)  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/shalev-atsis-software-developer)

---

For more detailed documentation and screenshots, see `Multi Threaded Chat Server.pdf`.
