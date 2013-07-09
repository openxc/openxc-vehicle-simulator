import socket
import threading
import time

class EnablerConnection():
    def __init__(self):
        self.initialize_data()
        print 'Enabler Connection created!'

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
        # print 'Sending ' + outString
        self.conn.sendall(outString)

    def initialize_data(self):
        self.steeringWheelAngle = 0
        print 'steeringWheelAngle initialized.'

    def update_angle(self, angle):
        self.steeringWheelAngle = angle

    def send_loop(self):
        try:
            self.create_socket_connection('', 50015)
        except Exception as e:
            print 'Network creation failed.'
            print e
        else:
            #This blocks until we get a connection.
            self.connected = True
            # TODO:  Add other loops with different delays.
            while self.connected == True:
                self.send("{\"name\":\"steering_wheel_angle\",\"value\":\"" + str(self.steeringWheelAngle) + "\"}\n")
                time.sleep(0.1)

    def start(self):
        t = threading.Thread(target=self.send_loop)
        t.setDaemon(True)
        t.start()
     
