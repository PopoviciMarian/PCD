import socket
import logging
import sys
import time
import os
from contextlib import contextmanager
logging.basicConfig(stream=sys.stdout, format='[%(levelname)s][%(asctime)s][%(pathname)s - %(funcName)s - %(lineno)d] - %(message)s', level=logging.INFO)
from functools import lru_cache 


@contextmanager
def get_send_handler(protocol, mechanism):
    _socket = None
    _socket_send = None
    if protocol == 'TCP':
        logging.info('Creating TCP socket')
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(('server',  int(os.environ.get('SERVER_PORT', 1234))))
    elif protocol == 'UDP':
        logging.info('Creating UDP socket')
        #_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket_send.bind(('client',  int(os.environ.get('CLIENT_PORT', 1236))))
        _socket_send.settimeout(5)
        _socket = _socket_send 
    else:
        raise ValueError('Invalid protocol')

    def send_streaming_handler(chunk):
        if protocol == 'TCP':
            _socket.send(chunk)
        elif protocol == 'UDP':
            _socket.sendto(chunk, ('server',  int(os.environ.get('SERVER_PORT', 1234))))


    def send_stop_and_wait_handler(chunk):
        chunk_size = len(chunk)
        if protocol == 'TCP':
            _socket.send(chunk)
            while True:
                try:
                    response = _socket.recv(chunk_size)
                    if int.from_bytes(response, 'big') == chunk_size:
                        break
                except socket.timeout:
                    logging.info('Timeout, resending chunk')
                    _socket.send(chunk)
        
        elif protocol == 'UDP':
            _socket.sendto(chunk, ('server',  int(os.environ.get('SERVER_PORT', 1234))))
            while True:
                try:
                    response, _ = _socket_send.recvfrom(4)
                    if int.from_bytes(response, 'big') == chunk_size:
                        break
                except socket.timeout:
                    logging.info('Timeout, resending chunk')
                    _socket_send.sendto(chunk, ('server',  os.environ.get('SERVER_PORT')))
          
    
    if mechanism == 'STREAMING':
        logging.info('Using streaming mechanism')
        yield send_streaming_handler
    elif mechanism == 'STOP_AND_WAIT':
        logging.info('Using stop and wait mechanism')
        yield send_stop_and_wait_handler
    
    _socket.close()
    if protocol == 'UDP':
        _socket_send.close()

class Client:
    def __init__(self, protocol, mechanism):
        self.protocol = protocol
        self.mechanism = mechanism
        self.send_handler = None
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', 1024))
        

    def send(self, file_path):
        bytes_sent = 0
        chunks_sent = 0
        file = open(file_path, 'rb')
        file_content = file.read()
        file.close()
        chunks =[file_content[i:i+self.chunk_size] for i in range(0, len(file_content), self.chunk_size)]
        logging.info(f'File {file_path} has {len(chunks)} chunks')
        with get_send_handler(self.protocol, self.mechanism) as handler:
            start = time.time()
            self.send_handler = handler
            for buffer in chunks:   
                self.send_handler(buffer)
                bytes_sent += len(buffer)
                chunks_sent += 1
            self.send_handler(b'')
        logging.info('File sent successfully')
        logging.info(f'Bytes sent: {bytes_sent} - Chunks sent: {chunks_sent}')
        logging.info(f'Time elapsed: {time.time() - start} seconds')


if __name__ == '__main__':
    client = Client(os.environ.get('PROTOCOL'), os.environ.get('MECHANISM'))
    client.send(os.environ.get('FILE_NAME'))