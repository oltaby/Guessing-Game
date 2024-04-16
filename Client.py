from socket import socket, AF_INET, SOCK_STREAM, error
import struct

import sys  # Import the sys module to access command-line arguments
# ... (rest of your code) ...


if len(sys.argv) != 3:
    print("Usage: python3 client.py <hostname> <port>")
    sys.exit(1)

hostname = sys.argv[1]
port = int(sys.argv[2])

server_addr = (hostname, port)
    
packer = struct.Struct('c I')

operators = ['<', '>', '=']
last_num = last_n_num = last_i_num = 0
last_op = last_n_op = last_i_op = ''

try:
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect(server_addr)

        lowest_num = 1
        highest_num = 100
        mid = lowest_num + (highest_num - lowest_num) // 2
        sent_op = operators[mid % (len(operators) - 1)]
        range_nums = [mid]

        packed_data = packer.pack(sent_op.encode(), int(mid))
        print('Client make starting guess')
        client.sendall(packed_data)

        while True:
            try:
                data = client.recv(packer.size)
                unp_data = packer.unpack(data)
                response = unp_data[0].decode()

                if response == 'V':
                    print('Someone else won')
                    client.close()
                    exit(0)
                elif response == 'Y':
                    print(f'Client won! The answer is {mid}')
                    client.close()
                    exit(0)
                elif response == 'K':
                    print('Client lose')
                    exit(0)
                else:
                    if response == 'I':
                        if sent_op == '<':
                            highest_num = mid - 1
                        elif sent_op == '>':
                            lowest_num = mid + 1
                    if response == 'N':
                        if sent_op == '<':
                            lowest_num = mid + 1
                        elif sent_op == '>':
                            highest_num = mid - 1

                    mid = lowest_num + (highest_num - lowest_num) // 2

                    if mid in range_nums:
                        sent_op = '='
                    else:
                        range_nums.append(mid)

                    if highest_num == lowest_num:
                        sent_op = '='
                    elif highest_num - lowest_num == 1:
                        mid = lowest_num
                        packed_data = packer.pack('<'.encode(), int(mid))
                        client.sendall(packed_data)
                        data = client.recv(packer.size)
                        unp_data = packer.unpack(data)
                        response = unp_data[0].decode()
                        if response == 'I':
                            mid = highest_num
                        else:
                            mid = lowest_num
                        sent_op = '='
                    else:
                        sent_op = operators[mid % (len(operators) - 1)]

                    print('Client make another guess')
                    packed_data = packer.pack(sent_op.encode(), int(mid))
                    client.sendall(packed_data)
            except error as e:
                print(f"Error while communicating with the server: {e}")
                break

except error as e:
    print(f"Socket error: {e}")
