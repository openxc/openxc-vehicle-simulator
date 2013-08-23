import socket
import threading

class EnablerConnection():
    def __init__(self):
        self.connections = []

        self.stopped = False

        self.local_ip = socket.gethostbyname(socket.gethostname())

        t = threading.Thread(target=self.listen_loop, name="Thread-connections")
        t.setDaemon(True)
        t.start()

    def create_socket_connection(self, host, port):
        #create the network socket connection
        print('Creating connection...')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen(1)
        print('Listening for a connection on port ' + str(port) + '...')
        self.conn, self.addr = self.s.accept()
        print('Connection established.')

    def send(self, outString):
        for connection in self.connections:
            try:
                connection.sendall(outString)
            except Exception:
                # TODO:  Isolate dropped connection, recover from other things.
                # For now, no recovery.  If ANYTHING goes wrong, drop the
                # connection.
                self.connections.remove(connection)
                print("Connection dropped.")

    def listen_loop(self):
        port = 50001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        self.s.listen(1)
        print('For the UI, navigate a browser to ' + str(self.local_ip) + ':5000')
        print('Set OpenXC Enabler network connections to ' + str(self.local_ip) + ', port ' + str(port))
        while True:
            conn, addr = self.s.accept()
            print("New connection to " + str(addr))
            self.connections.append(conn)

    def send_measurement(self, name, value):
        self.send("{\"name\":\"" + name + "\",\"value\":" + str(value) + "}\n")
