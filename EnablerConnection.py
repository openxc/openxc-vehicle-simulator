import socket
import threading
import time

class EnablerConnection():
    def __init__(self):
        self.initialize_data()
        print 'Enabler Connection created!'

        self.Connections = []

        self.Stopped = False
        
        t = threading.Thread(target=self.listen_loop)
        t.setDaemon(True)
        t.start()

        t2 = threading.Thread(target=self.send_loop)
        t2.setDaemon(True)
        t2.start()

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

    def send(self, outString, conn):
        # print 'Sending ' + outString
        conn.sendall(outString)

    def initialize_data(self):
        self.steeringWheelAngle = 0
        print 'steeringWheelAngle initialized.'

    def update_angle(self, angle):
        self.steeringWheelAngle = angle

    def listen_loop(self):
        port = 50001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))                
        self.s.listen(1)
        print 'Listening for a connection on port ' + str(port) + '...'
        while True:
            conn, addr = self.s.accept()
            print "New connection received."
            self.Connections.append(conn)

    def send_loop(self):
        while True:
            if not self.Stopped:
                self.SingleUpdate()
                time.sleep(0.16)

    def Pause(self):
        self.Stopped = True

    def Resume(self):
        self.Stopped = False

    def SingleUpdate(self):
        for connection in self.Connections:
            try:
                self.send("{\"name\":\"steering_wheel_angle\",\"value\":" + str(self.steeringWheelAngle) + ".0}\n", connection)
            except:
                #No recovery.  If ANYTHING goes wrong, drop the connection.
                self.Connections.remove(connection)
                print "Connection dropped."
