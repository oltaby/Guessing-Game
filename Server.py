import socket
import select
import struct
import random
import sys


class GuessingGameTCPSelectServer:
    def __init__(self, addr, port, timeout=1):
        self.server = self.setupServer(addr, port)
        self.inputs = [self.server]
        self.timeout = timeout
        self.packer = struct.Struct('c I')
        self.answer = ''
        self.correct_num = random.randint(1, 100)
        self.game_over = False

    def setupServer(self, addr, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (addr, port)
        server.bind(server_address)
        server.listen(5)
        return server

    def handleNewConnection(self, sock):
        connection, client_address = sock.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        print('Connected: %s:%d' % client_address)

    def handleDataFromClient(self, sock):
        data = sock.recv(self.packer.size)
        if data:
            print('Received:', data)
            unp_data = self.packer.unpack(data)
            print('Unpack:', unp_data)
            print(self.correct_num); 

            if self.game_over:
                self.answer = 'V'  # Game is over
            else:
                if unp_data[0].decode() == '=':
                    if self.correct_num == int(unp_data[1]):
                        self.answer = 'Y'  # Win
                        self.game_over = True
                        self.correct_num = random.randint(1, 100)
                    else:
                        self.answer = 'K'  # Lose
                        # self.game_over = True
                elif unp_data[0].decode() == '>':
                    if self.correct_num > int(unp_data[1]):
                        self.answer = 'I'  # Yes
                    else:
                        self.answer = 'N'  # No
                elif unp_data[0].decode() == '<':
                    if self.correct_num < int(unp_data[1]):
                        self.answer = 'I'  # Yes
                    else:
                        self.answer = 'N'  # No

            data = self.packer.pack(str(self.answer).encode(), 0)
            sock.sendall(data)
            print('Evaluated and sent back: %s' % self.answer)
            print('Genereted Number:', self.correct_num)
        else:
            self.inputs.remove(sock)
            sock.close()

    def handleInputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handleNewConnection(sock)
            else:
                self.handleDataFromClient(sock)

    def handleExceptionalCondition(self, exceptional):
        for sock in exceptional:
            self.inputs.remove(sock)
            sock.close()

    def handleConnections(self):
        while self.inputs:
            try:
                readable, _, exceptional = select.select(self.inputs, [], self.inputs, self.timeout)
                
                if not (readable or exceptional):
                    continue

                self.handleInputs(readable)
                self.handleExceptionalCondition(exceptional)
            except KeyboardInterrupt:
                print("Server closing")
                for c in self.inputs:
                    c.close()
                self.inputs = []
                
if len(sys.argv) == 3:
    guessingGameTCPSelectServer = GuessingGameTCPSelectServer(sys.argv[1], int(sys.argv[2]))
else:
    guessingGameTCPSelectServer = GuessingGameTCPSelectServer()
guessingGameTCPSelectServer.handleConnections()


