import socket

class EnablerConnection():
    def __init__(self):
        print 'Enabler Connection created!'

    def create_socket_connection(self, host, port):
        #create the network socket connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen(1)
        print 'listening for a connection...'
        self.conn, self.addr = self.s.accept()
        print 'Connection established.'

    def send(self, outString):
        print 'Sending ' + outString
        self.conn.sendall(outString)
