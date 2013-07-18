import enabler_connection
import dynamics_model
import threading
import time

class StateManager(object):
    def __init__(self):
        self.stopped = False
        self.initialize_data()
        self.connection = enabler_connection.EnablerConnection()
        self.dynamics_model = dynamics_model.DynamicsModel()

        t = threading.Thread(target=self.send_loop_6Hz, name="Thread-6Hz")
        t.setDaemon(True)
        t.start()

        print('State Manager initialized')

    def initialize_data(self):
        self.steering_wheel_angle = 0

    @property
    def accelerator_pedal_position(self):
        return self.dynamics_model.accelerator

    @accelerator_pedal_position.setter
    def accelerator_pedal_position(self, value):
        self.dynamics_model.accelerator = value

    def send_loop_6Hz(self):
        sleep_duration = 1.0 / (6 * 3)  # 1 second / 6Hz, / # of data points.
        while True:
            if not self.stopped:
                self.connection.send_measurement("accelerator_pedal_position",
                        self.dynamics_model.accelerator)
                time.sleep(sleep_duration)
                self.connection.send_measurement("steering_wheel_angle",
                        self.steering_wheel_angle)
                time.sleep(sleep_duration)
                self.connection.send_measurement("vehicle_speed",
                        self.dynamics_model.vehicle_speed)
                time.sleep(sleep_duration)
            else:
                time.sleep(1.0 / 6)

    def pause(self):
        self.stopped = True

    def resume(self):
        self.stopped = False

    def update_once(self):
        self.connection.send_measurement("steering_wheel_angle", self.steering_wheel_angle)

    def local_ip(self):
        return self.connection.local_ip
