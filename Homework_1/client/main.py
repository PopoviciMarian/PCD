import socket
import logging
import sys
import time
import os
from contextlib import contextmanager

logging.basicConfig(stream=sys.stdout, format='[%(levelname)s][%(asctime)s][%(pathname)s - %(funcName)s - %(lineno)d] - %(message)s', level=logging.INFO)

@contextmanager
def get_send_handler(protocol, mechanism):
    _socket = None
    start = None
    try:
        if protocol == 'TCP':
            logging.info('Creating TCP socket')
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect(('server', int(os.environ.get('SERVER_PORT', 1234))))
            _socket.settimeout(1)
        elif protocol == 'UDP':
            logging.info('Creating UDP socket')
            _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 65536)
            _socket.settimeout(1)
        else:
            raise ValueError('Invalid protocol')

        def send_streaming_handler(chunk):
            if protocol == 'TCP':
                _socket.send(chunk)
            elif protocol == 'UDP':
                _socket.sendto(chunk, ('server', int(os.environ.get('SERVER_PORT', 1234))))
            
        def send_stop_and_wait_handler(chunk):
            if protocol == 'TCP':
                _socket.send(chunk)
                if len(chunk) < int(os.environ.get('CHUNK_SIZE', 1024)):
                    return
                while True:
                    try:
                        response = _socket.recv(3)
                        if response.decode('utf-8') == 'ack':
                            break
                    except socket.timeout:
                        logging.error('Timeout, resending chunk')
                        #_socket.send(chunk)
            
            elif protocol == 'UDP':
                _socket.sendto(chunk, ('server', int(os.environ.get('SERVER_PORT', 1234))))
                if len(chunk) < int(os.environ.get('CHUNK_SIZE', 1024)):
                    return
                while True:
                    try:
                        response, _ = _socket.recvfrom(3)
                        if response.decode('utf-8') == 'ack':
                            break
                    except socket.timeout:
                        logging.info('Timeout, resending chunk')
                        #_socket.sendto(chunk, ('server', int(os.environ.get('SERVER_PORT', 1234))))

        if mechanism == 'STREAMING':
            logging.info('Using streaming mechanism')
            start = time.time()
            yield send_streaming_handler
        elif mechanism == 'STOP_AND_WAIT':
            logging.info('Using stop and wait mechanism')
            start = time.time()
            yield send_stop_and_wait_handler
    finally:
        if start is not None:
            logging.info(f'Time elapsed: {time.time() - start} seconds')
        if _socket:
            _socket.close()

class Client:
    def __init__(self, protocol, mechanism):
        self.protocol = protocol
        self.mechanism = mechanism
        self.chunk_size = int(os.environ.get('CHUNK_SIZE', 1024)) 

    def send(self, file_path):
        bytes_sent = 0
        chunks_sent = 0
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                chunks = [file_content[i:i+self.chunk_size] for i in range(0, len(file_content), self.chunk_size)]
                logging.info(f'File {file_path} has {len(chunks)} chunks')
                with get_send_handler(self.protocol, self.mechanism) as send_handler:
                    for buffer in chunks:   
                        send_handler(buffer)
                        bytes_sent += len(buffer)
                        chunks_sent += 1
                    send_handler(b'')
                logging.info('File sent successfully')
                logging.info(f'Bytes sent: {bytes_sent} - Chunks sent: {chunks_sent}')
        except Exception as e:
            logging.error(f"Error occurred while sending file: {str(e)}")


if __name__ == '__main__':
    client = Client(os.environ.get('PROTOCOL'), os.environ.get('MECHANISM'))
    client.send(os.environ.get('FILE_NAME'))
