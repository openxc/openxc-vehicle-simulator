import enabler_connection
import dynamics_model
import threading
import time

class StateManager(object):
    def __init__(self):
        self.stopped = False
        self.connection = enabler_connection.EnablerConnection()
        self.dynamics_model = dynamics_model.DynamicsModel(
                self.connection.send_measurement)

        self.start_send_loop(self.send_loop_1Hz, "Thread-1Hz")
        self.start_send_loop(self.send_loop_4Hz, "Thread-4Hz")
        self.start_send_loop(self.send_loop_6Hz, "Thread-6Hz")
        self.start_send_loop(self.send_loop_10Hz, "Thread-10Hz")
        self.start_send_loop(self.send_loop_48Hz, "Thread-48Hz")
        self.start_send_loop(self.send_loop_60Hz, "Thread-60Hz")

        self.headlamp = False
        self.highbeams = False
        self.wipers = False
        self.door_status = {'driver':False, 'passenger':False,
                'left_rear':False, 'right_rear':False}

        print('State Manager initialized')

# Properties -------------------

    @property
    def steering_wheel_angle(self):
        return self.dynamics_model.steering_wheel_angle

    @steering_wheel_angle.setter
    def steering_wheel_angle(self, value):
        self.dynamics_model.steering_wheel_angle = value

    @property
    def accelerator_pedal_position(self):
        return self.dynamics_model.accelerator

    @accelerator_pedal_position.setter
    def accelerator_pedal_position(self, value):
        self.dynamics_model.accelerator = value

    @property
    def parking_brake_status(self):
        return self.dynamics_model.parking_brake_status

    @parking_brake_status.setter
    def parking_brake_status(self, value):
        if value != self.dynamics_model.parking_brake_status:
            self.connection.send_measurement("parking_brake_status", value)
        self.dynamics_model.parking_brake_status = value

    @property
    def brake_pedal_position(self):
        return self.dynamics_model.brake

    @brake_pedal_position.setter
    def brake_pedal_position(self, value):
        old_brake = self.dynamics_model.brake_pedal_status
        self.dynamics_model.brake = value
        if old_brake != self.dynamics_model.brake_pedal_status:
            self.connection.send_measurement("brake_pedal_status",
                        self.dynamics_model.brake_pedal_status)

    @property
    def ignition_status(self):
        return self.dynamics_model.ignition_status

    @parking_brake_status.setter
    def ignition_status(self, value):
        if value != self.dynamics_model.ignition_status:
            self.connection.send_measurement("ignition_status", value)
            self.dynamics_model.ignition_status = value

    @property
    def headlamp_status(self):
        return self.headlamp

    @parking_brake_status.setter
    def headlamp_status(self, value):
        if value != self.headlamp:
            self.connection.send_measurement("headlamp_status", value)
            self.headlamp = value

    @property
    def high_beam_status(self):
        return self.highbeam

    @parking_brake_status.setter
    def high_beam_status(self, value):
        if value != self.highbeam:
            self.connection.send_measurement("high_beam_status", value)
            self.headlamp = value

    @property
    def windshield_wiper_status(self):
        return self.wipers

    @windshield_wiper_status.setter
    def windshield_wiper_status(self, value):
        if value != self.wipers:
            self.connection.send_measurement("windshield_wiper_status", value)
            self.wipers = value

    @property
    def local_ip(self):
        return self.connection.local_ip

    @property
    def dynamics_data(self):
        return self.dynamics_model.data

# Sending Data ------------------

    def start_send_loop(self, function, thread_name):
        t = threading.Thread(target=self.send_loop, args=[function],
                name=thread_name)
        t.setDaemon(True)
        t.start()

    def send_loop(self, function):
        while True:
            if not self.stopped:
                function()
            else:
                time.sleep(0.5)

    def send_loop_1Hz(self):
        self.connection.send_measurement("latitude",
                        self.dynamics_model.lat)
        self.connection.send_measurement("longitude",
                        self.dynamics_model.lon)
        time.sleep(1.0)

    def send_loop_4Hz(self):
        self.connection.send_measurement("vehicle_speed",
                        self.dynamics_model.vehicle_speed)
        self.connection.send_measurement("engine_speed",
                        self.dynamics_model.engine_speed)
        time.sleep(1.0/4)

    def send_loop_6Hz(self):
        self.connection.send_measurement("steering_wheel_angle",
                        self.steering_wheel_angle)
        time.sleep(1.0/6)

    def send_loop_10Hz(self):
        self.connection.send_measurement("fuel_consumed_since_restart",
                        self.dynamics_model.fuel_consumed)
        self.connection.send_measurement("odometer",
                        self.dynamics_model.odometer)
        time.sleep(1.0/10)

    def send_loop_48Hz(self):
        self.connection.send_measurement("fuel_level",
                        self.dynamics_model.fuel_level)
        time.sleep(1.0/48)

    def send_loop_60Hz(self):
        self.connection.send_measurement("accelerator_pedal_position",
                        self.dynamics_model.accelerator)
        self.connection.send_measurement("torque_at_transmission",
                        self.dynamics_model.torque)
        time.sleep(1.0/60)

    def pause(self):
        self.stopped = True
        self.dynamics_model.stopped = True

    def resume(self):
        self.dynamics_model.stopped = False
        self.stopped = False

    def update_once(self):
        self.connection.send_measurement("steering_wheel_angle",
                self.steering_wheel_angle)

    def send_callback(self, data_name, value, event=None):
        self.connection.send_measurement(data_name, value, event)

    def update_door(self, door, value):
        self.door_status[door] = value
        self.connection.send_measurement("door_status", door, value)
