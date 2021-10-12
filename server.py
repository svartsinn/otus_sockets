import socket
import random
import logging
import threading
import urllib

from http.client import responses
from urllib.parse import parse_qs

logging.basicConfig(level=logging.DEBUG)

HOST = '127.0.0.1'
PORT = random.randint(10000, 20000)


class InvalidRequest(Exception):
    pass


def parse_request(request):
    temp = [i.strip() for i in request.splitlines()]

    if -1 == temp[0].find('HTTP'):
        raise InvalidRequest('Incorrect Protocol')

    method, path, protocol = [i.strip() for i in temp[0].split()]
    headers = {}
    if 'GET' == method:
        for k, v in [i.split(':', 1) for i in temp[1:-1]]:
            headers[k.strip()] = v.strip()
    else:
        raise InvalidRequest('Only accepts GET requests')

    return {'method': method,
            'path': path,
            'protocol': protocol,
            'headers': headers}


def on_new_client(conn, addr):
    data = conn.recv(1024)

    if data:
        req = parse_request(data.decode('utf-8'))
        response_status = None

        parsed_url = urllib.parse.urlparse(req['path'])
        params = parse_qs(parsed_url.query)
        for key, value in params.items():
            if key == 'status':
                response_status = value[0]
            else:
                response_status = 200

        response = 'Request Method: ' + req['method'] + '\n'
        response += f"Request Source: {addr}" + '\n'
        if response_status is not None:
            response += 'Response Status: ' + response_status + ' ' + responses[int(response_status)] + '\n'
        if req['headers'] is not None:
            for key, value in req['headers'].items():
                response += key + ': ' + value + '\n'
        print(response)
        response = response.encode('utf-8')
        conn.send(response)

    elif not data or data == b'close':
        print('Got termination signal', data, 'and closed connection')
        conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'Binding server on {HOST}:{PORT}')
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
    conn.send('Hello, I am server!\n'.encode('utf-8'))
    threading.Thread(target=on_new_client,
                     args=(conn, addr)).start()
