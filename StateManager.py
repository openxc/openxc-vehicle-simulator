import EnablerConnection
import threading
import time

class StateManager():
    def __init__(self):
        self.Stopped = False
        self.initialize_data()
        self.Conn = EnablerConnection.EnablerConnection()

        t = threading.Thread(target=self.send_loop_6Hz)
        t.setDaemon(True)
        t.start()
        
        print 'State Manager initialized'

    def initialize_data(self):
        self.steeringWheelAngle = 0

    def update_angle(self, angle):
        self.steeringWheelAngle = angle

    def send_loop_6Hz(self):
        while True:
            if not self.Stopped:
                self.SingleUpdate()
                time.sleep(0.16)

    def Pause(self):
        self.Stopped = True

    def Resume(self):
        self.Stopped = False

    def SingleUpdate(self):
        self.Conn.send("{\"name\":\"steering_wheel_angle\",\"value\":" + str(self.steeringWheelAngle) + ".0}\n")
