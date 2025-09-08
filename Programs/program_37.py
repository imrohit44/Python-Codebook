import selectors
import socket

class NonBlockingEchoServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.bind((self.host, self.port))
        sock.listen()

        self.selector.register(sock, selectors.EVENT_READ, data=None)

        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_connection(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_connection(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        data = {'addr': addr, 'inb': b'', 'outb': b''}
        self.selector.register(conn, selectors.EVENT_READ, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data['outb'] += recv_data
                self.selector.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data)
            else:
                self.selector.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data['outb']:
                sent = sock.send(data['outb'])
                data['outb'] = data['outb'][sent:]
                if not data['outb']:
                    self.selector.modify(sock, selectors.EVENT_READ, data)

if __name__ == "__main__":
    server = NonBlockingEchoServer()
    server.start()