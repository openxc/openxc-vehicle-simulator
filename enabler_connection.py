import socket
import threading
import json

class EnablerConnection():
    def __init__(self):
        self.connections = []

        self.stopped = False
        self.enabler_listening_port = 50001

        self.local_ip = socket.gethostbyname(socket.gethostname())
        t = threading.Thread(target=self.listen_loop, name='0.0.0.0',
                args=('0.0.0.0',))
        t.setDaemon(True)
        t.start()

    def send(self, outString):
        for socket_handler in self.connections:
            try:
                socket_handler.send(outString)
            except Exception as e:
                # TODO:  Isolate dropped connection, recover from other things.
                # For now, no recovery.  If ANYTHING goes wrong, drop the
                # connection.
                print("Exception while sending data: %s" % e)
                self.connections.remove(socket_handler)
                print("Connection dropped.")

    def listen_loop(self, this_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((this_ip, self.enabler_listening_port))
        s.listen(1)
        print("Listening for OpenXC Enabler on " + this_ip + ":" +
                str(self.enabler_listening_port))
        while True:
            conn, addr = s.accept()
            print("New connection to " + this_ip + " from " + str(addr))
            handler = SocketHandler(conn, addr)
            handler.start()
            self.connections.append(handler)

    def send_measurement(self, name, value, event=None):
        data = {'name':name,'value':value}
        if event is not None and event != '':
            data['event'] = event
        self.send_json(json.dumps(data))

    def send_json(self, json_payload):
        self.send(json_payload + '\x00')

    def received_messages(self):
        all_received_data = ''.join(handler.received_command_data for handler in
                self.connections)
        return all_received_data.split('\0')

class SocketHandler(threading.Thread):
    def __init__(self, connection, address):
        super(SocketHandler, self).__init__()
        self.daemon = True
        self.connection = connection
        self.address = address
        self.received_command_data = ""

    def send(self, data):
        self.connection.sendall(data)

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if not data:
                break
            else:
                self.received_command_data += data
