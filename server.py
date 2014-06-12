import config, socket, threading, struct, pickle
from lib import in_cmd, out_cmd, handlers

__NAME__ = 'SublimeTogetherServer'
__VERSION__ = '0.0.3'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((config.host, config.port))
server.listen(0)
print('%s/%s listen at: %s:%s' % (__NAME__, __VERSION__, config.host, config.port))

pool = []

class SocketHandlerThread(threading.Thread):
    '''Handler class for each socket connection from client'''

    user_name = ""
    socket = None
    address = None
    enabled = True

    head = [0xa9, 0x5f, 0xca]

    def __init__(self, socket, address):
        super(SocketHandlerThread, self).__init__()
        self.socket = socket
        self.address = address
        print('%s:%s connected' % address)

    def run(self):
        global config
        try:
            self.send('message', '[%s/%s] Server connected.' % (__NAME__, __VERSION__))
            while self.enabled:
                self.read_command()
        except ConnectionError as err:
            print(err)
        finally:
            self.socket.close()
            remove_thread(self)

    def read_command(self, offset = 0):
        '''read command from client'''
        try:
            byte = self.socket.recv(1)[0]
        except IndexError as err:
            raise ConnectionError("Client %s:%s disconnected." % self.address)
        if byte == self.head[offset]:
            if offset is 2:
                tmp = self.socket.recv(5)
                # convert 4 bytes data to unsigned integer (I), offset 1
                length = struct.unpack_from('I', tmp, 1)[0]
                data = self.socket.recv(length)
                data = pickle.loads(data)
                key = tmp[0]
                if key in in_cmd:
                    cmd = in_cmd[tmp[0]]
                else:
                    cmd = 'error'
                handlers.__dict__['%s_handler' % cmd](key, data, pool, self)
            else:
                self.read_command(offset + 1)
        else:
            print('error byte:')
            print(byte)

    def send(self, cmd, data):
        out = pickle.dumps(data)
        # send header
        header = b'\xd0\x02\x0f'
        # send command
        command = out_cmd[cmd].to_bytes(1, 'big')
        # send data-length
        length = len(out).to_bytes(4, 'little')
        # send all data
        all_data = header + command + length + out
        # print('all_data:', all_data)
        self.socket.sendall(header + command + length + out)

    def close(self):
        self.enabled = False
        print('Connection for %s:%s closed.' % self.address)

def remove_thread(thread):
    '''remove spicified thread from the pool'''
    global pool
    new_pool = []
    for item in pool:
        if item is not thread:
            new_pool.append(item)
    pool = new_pool

def clear_pool():
    '''remove dead threads in the pool'''
    global pool
    new_pool = []
    for item in pool:
        if item.is_alive():
            new_pool.append(item)
    pool = new_pool


while True:
    sock, addr = server.accept()
    thread = SocketHandlerThread(sock, addr)
    pool.append(thread)
    thread.start()
