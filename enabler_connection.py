import socket
import threading

class EnablerConnection():
    def __init__(self):
        self.connections = []

        self.stopped = False

        self.local_ip = socket.gethostbyname(socket.gethostname())
        #self.local_ip = '192.168.1.8'

        t = threading.Thread(target=self.listen_loop, name="Thread-connections")
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

    def listen_loop(self):
        port = 50001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((str(self.local_ip), port))
        self.s.listen(1)
        print('For the UI, navigate a browser to ' + str(self.local_ip) + ':5000')
        print('Set OpenXC Enabler network connections to ' + str(self.local_ip) + ', port ' + str(port))
        while True:
            conn, addr = self.s.accept()
            print("New connection to " + str(addr))
            self.connections.append(conn)

    def send_measurement(self, name, value):
        if (type(value) == bool):
            if value:
                value = "true"
            else:
                value = "false"
        extra_quote = "\""
        if(type(value) != unicode):
            extra_quote = ""
        send_string = "{\"name\":\"" + name + "\",\"value\":" + extra_quote + str(value) + extra_quote + "}\n"
        self.send(send_string)

    def send_event(self, name, value, event):
        if (type(value) == bool):
            if value:
                value = "true"
            else:
                value = "false"
        if (type(event) == bool):
            if event:
                event = "true"
            else:
                event = "false"
        send_string = "{\"name\":\"" + name + "\",\"value\":\"" + str(value) + "\",\"event\":" + str(event) + "}\n"
        self.send(send_string)
