import EnablerConnection
import DynamicsModel
import threading
import time

class StateManager():
    def __init__(self):
        self.Stopped = False
        self.initialize_data()
        self.Conn = EnablerConnection.EnablerConnection()
        self.VDM = DynamicsModel.DynamicsModel()

        t = threading.Thread(target=self.send_loop_6Hz, name="Thread-6Hz")
        t.setDaemon(True)
        t.start()
        
        print 'State Manager initialized'

    def initialize_data(self):
        self.steering_wheel_angle = 0
        self.accelerator = 0.0

    def update_angle(self, angle):
        self.steering_wheel_angle = angle

    def get_angle(self):
        return self.steering_wheel_angle

    def get_accelerator(self):
        return self.accelerator

    def update_accelerator(self, new_value):
        self.accelerator = new_value
        self.VDM.set_accel(new_value)

    def send_loop_6Hz(self):
        sleep_duration = 1.0 / (6 * 3)  # 1 second / 6Hz, / # of data points.
        while True:
            if not self.Stopped:
                self.Conn.send_JSON("accelerator_pedal_position", self.accelerator)
                time.sleep(sleep_duration)
                self.Conn.send_JSON("steering_wheel_angle", self.steering_wheel_angle)
                time.sleep(sleep_duration)
                self.Conn.send_JSON("vehicle_speed", self.VDM.get_vehicle_speed())
                time.sleep(sleep_duration)
            else:
                time.sleep(1.0 / 6)

    def pause(self):
        self.Stopped = True

    def resume(self):
        self.Stopped = False

    def update_once(self):
        self.Conn.send_JSON("steering_wheel_angle", self.steering_wheel_angle)

    def local_IP(self):
        return self.Conn.local_IP()
