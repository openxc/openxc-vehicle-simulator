import socket
import threading
import json

class EnablerConnection():
    def __init__(self):
        self.connections = []

        self.stopped = False
        self.enabler_listening_port = 50001

        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
        #self.local_ip = '192.168.1.8'

        for ip in self.ip_list:
            t = threading.Thread(target=self.listen_loop, name=ip, args=(ip,))
            t.setDaemon(True)
            t.start()

    def send(self, outString):
        for connection in self.connections:
            try:
                connection.sendall(outString)
            except Exception:
                # TODO:  Isolate dropped connection, recover from other things.
                # For now, no recovery.  If ANYTHING goes wrong, drop the
                # connection.
                print("Exception while sending data: " + Exception)
                self.connections.remove(connection)
                print("Connection dropped.")

    def listen_loop(self, this_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((this_ip, self.enabler_listening_port))
        s.listen(1)
        print("Listening for OpenXC Enabler on " + this_ip + ":" + str(self.enabler_listening_port))
        while True:
            conn, addr = s.accept()
            print("New connection to " + this_ip + " from " + str(addr))
            self.connections.append(conn)

    def send_measurement(self, name, value):
        send_string = json.dumps({'name':name,'value':value})
        self.send(send_string + "\n")

    def send_event(self, name, value, event):
        send_string = json.dumps({'name':name,'value':value,'event':event})
        self.send(send_string + "\n")
