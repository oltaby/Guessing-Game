# Question / Answer Game

This application implements a question and answer game where clients connect to a server, which has chosen a random integer between 1 and 100. Clients use a logarithmic search algorithm to guess the number. Upon guessing correctly, the server sends an "End" message to all clients, terminating the game.

## Server Implementation:
- The server serves multiple clients concurrently using the SELECT function.
- It chooses a random integer between 1 and 100.
- It communicates with clients using TCP.
- Upon receiving a correct guess from any client, it sends an "End" message to all clients, terminating the game.

## Client Implementation:
- The client connects to the server using TCP.
- It uses a logarithmic search algorithm to guess the number chosen by the server.
- It sends its guesses to the server and receives responses.
- Upon receiving a "Win" message, it terminates the connection.
- It handles messages from the server, including "Yes", "No", "Quit", "Win", and "End".

## Message Format:
- From Client: Bytes format with one character and one integer (struct). The character indicates the relationship of the guess to the chosen number ("<" for smaller, ">" for bigger, "=" for equals).
- From Server: Same bytes format, but the character indicates the server's response ("I" for Yes, "N" for No, "K" for Quit, "Y" for Win, "V" for End).

## Usage:
1. **Server:** `python3 server.py <hostname> <port_number>`
   - Example: `python3 server.py localhost 10000`
2. **Client:** `python3 client.py <hostname> <port_number>`
   - Example: `python3 client.py localhost 10000`

**Note:**
- Ensure both `server.py` and `client.py` files are present in the same directory.
- Replace `<hostname>` and `<port_number>` with the appropriate values for your setup.
