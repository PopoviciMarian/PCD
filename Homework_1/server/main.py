import socket
import logging
import sys
import time
import os
from contextlib import contextmanager
logging.basicConfig(stream=sys.stdout, format='[%(levelname)s][%(asctime)s][%(pathname)s - %(funcName)s - %(lineno)d] - %(message)s', level=logging.INFO)

@contextmanager
def get_recv_handler(protocol, mechanism):
    _socket = None

    if protocol == 'TCP':
        logging.info('Creating TCP socket')
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
        _socket.bind(('server', int(os.environ.get('SERVER_PORT'))))
        _socket.listen(1)
        conn, _ = _socket.accept()
    elif protocol == 'UDP':
        logging.info('Creating UDP socket')
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.bind(('server', int(os.environ.get('SERVER_PORT', 1234))))
        _socket.settimeout(5)

    def recv_streaming_handler(chunk_size):
        if protocol == 'TCP':
            return conn.recv(chunk_size)
        elif protocol == 'UDP':
            try:
                data, _ = _socket.recvfrom(chunk_size)
                return data
            except socket.timeout:
                return b''
        
    def recv_stop_and_wait_handler(chunk_size):
        if protocol == 'TCP':
            chunk =  conn.recv(chunk_size)
            conn.send('ack'.encode('utf-8'))
            return chunk
        elif protocol == 'UDP':
            data, addr = _socket.recvfrom(chunk_size)
            _socket.sendto('ack'.encode('utf-8'), addr)
            return data
        
    if mechanism == 'STREAMING':
        logging.info('Using streaming mechanism')
        yield recv_streaming_handler
    elif mechanism == 'STOP_AND_WAIT':
        logging.info('Using stop and wait mechanism')
        yield recv_stop_and_wait_handler
    else:
        raise ValueError('Invalid mechanism')
    
    if protocol == 'TCP':
        conn.close()

    _socket.close()

class Server():
    def __init__(self, protocol, mechanism):
        self.protocol = protocol
        self.mechanism = mechanism
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', 1024))

    def start(self):
       # map_timestamp_chunk_size = {}
        bytes_recv = 0
        chunks_recv = 0
        file_name = os.environ.get('FILE_NAME')
        with get_recv_handler(self.protocol, self.mechanism) as recv_handler:
            chunk = recv_handler(self.chunk_size)
            start = time.time()
            while True:
                if not chunk or len(chunk) == 0:
                    break
                #if(len(chunk) != 1024):
               #     logging.info(f'Last chunk size: {len(chunk)}')
             #   map_timestamp_chunk_size[time.time()] = len(chunk)
                bytes_recv += len(chunk)
                chunks_recv += 1
                chunk = recv_handler(self.chunk_size)
            logging.info(f'File received: {file_name}')
            logging.info(f'Bytes received: {bytes_recv} - Chunks received: {chunks_recv}')
            logging.info(f'Time elapsed: {time.time() - start} seconds')

if __name__ == '__main__':
    server = Server(os.environ.get('PROTOCOL'), os.environ.get('MECHANISM'))
    server.start()
