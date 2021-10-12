import socket
import sys

HOST = '127.0.0.1'
PORT = None

try:
    PORT = int(sys.argv[1])
except IndexError:
    print('Pass a port for connection')
    exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f'Connecting to {HOST}:{PORT}')
    s.connect((HOST, PORT))
    data = s.recv(1024)
    print(repr(data))

    while True:
        data_to_send = 'GET http://example.ir/index.php HTTP/1.0 Accept: text/plain\n\n'

        if data_to_send == 'close':
            s.send(bytes(data_to_send.strip(), 'utf-8'))
            print('Close connection')
            break

        s.send(bytes(data_to_send.encode('utf-8')))
        data = s.recv(1024)

        print('Received back:', repr(data.decode('utf-8')))
