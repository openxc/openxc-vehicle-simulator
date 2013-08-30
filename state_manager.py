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

        self.SLEEP_4HZ = 1.0 / (4 * 2)  # 1 second / 4Hz, / # of data points.
        self.start_send_loop(self.send_loop_4Hz, "Thread-4Hz")
        self.SLEEP_6HZ = 1.0 / (6 * 1)  # 1 second / 6Hz, / # of data points.
        self.start_send_loop(self.send_loop_6Hz, "Thread-6Hz")
        self.SLEEP_10HZ = 1.0 / (10 * 2)  # 1 second / 6Hz, / # of data points.
        self.start_send_loop(self.send_loop_10Hz, "Thread-10Hz")
        self.SLEEP_60HZ = 1.0 / (60 * 2)  # 1 second / 6Hz, / # of data points.
        self.start_send_loop(self.send_loop_60Hz, "Thread-60Hz")

        print('State Manager initialized')

    def initialize_data(self):
        self.steering_wheel_angle = 0

# Properties -------------------

    @property
    def accelerator_pedal_position(self):
        return self.dynamics_model.accelerator

    @accelerator_pedal_position.setter
    def accelerator_pedal_position(self, value):
        self.dynamics_model.accelerator = value

    @property
    def brake_pedal_position(self):
        return self.dynamics_model.brake

    @brake_pedal_position.setter
    def brake_pedal_position(self, value):
        old_brake = self.dynamics_model.brake_pedal_status
        self.dynamics_model.brake = value
        if old_brake != self.dynamics_model.brake_pedal_status:
            print "sending"
            self.connection.send_measurement("brake_pedal_status",
                        self.dynamics_model.brake_pedal_status)

    @property
    def local_ip(self):
        return self.connection.local_ip

    @property
    def vehicle_speed(self):
        return self.dynamics_model.vehicle_speed

    @property
    def fuel_consumed(self):
        return self.dynamics_model.fuel_consumed

    @property
    def dynamics_data(self):
        return self.dynamics_model.data

# Sending Data ------------------

    def start_send_loop(self, function, thread_name):
        t = threading.Thread(target=self.send_loop, args=[function], name=thread_name)
        t.setDaemon(True)
        t.start()

    def send_loop(self, function):
        while True:
            if not self.stopped:
                function()
            else:
                time.sleep(0.5)

    def send_loop_4Hz(self):
        self.connection.send_measurement("vehicle_speed",
                        self.dynamics_model.vehicle_speed)
        time.sleep(self.SLEEP_4HZ)
        self.connection.send_measurement("engine_speed",
                        self.dynamics_model.engine_speed)
        time.sleep(self.SLEEP_4HZ)

    def send_loop_6Hz(self):
        self.connection.send_measurement("steering_wheel_angle",
                        self.steering_wheel_angle)
        time.sleep(self.SLEEP_6HZ)

    def send_loop_10Hz(self):
        self.connection.send_measurement("fuel_consumed_since_restart",
                        self.dynamics_model.fuel_consumed)
        time.sleep(self.SLEEP_10HZ)
        self.connection.send_measurement("odometer",
                        self.dynamics_model.odometer)
        time.sleep(self.SLEEP_10HZ)

    def send_loop_60Hz(self):
        self.connection.send_measurement("accelerator_pedal_position",
                        self.dynamics_model.accelerator)
        time.sleep(self.SLEEP_60HZ)
        self.connection.send_measurement("torque_at_transmission",
                        self.dynamics_model.torque)
        time.sleep(self.SLEEP_60HZ)
        
    def pause(self):
        self.stopped = True

    def resume(self):
        self.stopped = False

    def update_once(self):
        self.connection.send_measurement("steering_wheel_angle", self.steering_wheel_angle)
