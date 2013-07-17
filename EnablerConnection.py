import socket
import threading

class EnablerConnection():
    def __init__(self):
        self.Connections = []

        self.Stopped = False
        
        t = threading.Thread(target=self.listen_loop, name="Thread-Connections")
        t.setDaemon(True)
        t.start()

        self.local_ip = socket.gethostbyname(socket.gethostname())

    def create_socket_connection(self, host, port):
        #create the network socket connection
        print 'Creating connection...'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))                
        self.s.listen(1)
        print 'Listening for a connection on port ' + str(port) + '...'
        self.conn, self.addr = self.s.accept()
        print 'Connection established.'

    def send(self, outString):
        for connection in self.Connections:
            try:
                connection.sendall(outString)
            except Exception as e:
                #TODO:  Isolate dropped connection, recover from other things.
                #For now, no recovery.  If ANYTHING goes wrong, drop the connection.
                self.Connections.remove(connection)
                print "Connection dropped."

    def listen_loop(self):
        port = 50001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))                
        self.s.listen(1)
        print 'Listening for a connection on port ' + str(port) + '...'
        while True:
            conn, addr = self.s.accept()
            print "New connection to " + str(addr)
            self.Connections.append(conn)

    def send_JSON(self, name, value):
        self.send("{\"name\":\"" + name + "\",\"value\":" + str(value) + "}\n")

    def local_IP(self):
        return self.local_ip
