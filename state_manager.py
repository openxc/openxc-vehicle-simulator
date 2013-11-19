import enabler_connection
import dynamics_model
import threading
import time
import datetime

class StateManager(object):
    def __init__(self):
        self.stopped = False
        self.connection = enabler_connection.EnablerConnection()
        self.dynamics_model = dynamics_model.DynamicsModel(
                self.connection.send_measurement)

        self.headlamp = False
        self.highbeams = False
        self.wipers = False
        self.door_status = {'driver':False, 'passenger':False,
                'left_rear':False, 'right_rear':False}

        self.start_send_loop(self.send_loop_1Hz, "Thread-1Hz")
        self.start_send_loop(self.send_loop_10Hz, "Thread-10Hz")
        self.start_send_loop(self.send_loop_48Hz, "Thread-48Hz")

        self.data = []

        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'steering_wheel_angle',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False})

        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'torque_at_transmission',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False})

        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'engine_speed',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False})

        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'vehicle_speed',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False})

        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'accelerator_pedal_position',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False})

        self.start_send_loop(self.send_all_loop, "Send-Thread")
        

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

    @ignition_status.setter
    def ignition_status(self, value):
        if value != self.dynamics_model.ignition_status:
            self.connection.send_measurement("ignition_status", value)
            self.dynamics_model.ignition_status = value

    @property
    def gear_lever_position(self):
        return self.dynamics_model.gear_lever_position

    @gear_lever_position.setter
    def gear_lever_position(self, value):
        if value != self.dynamics_model.gear_lever_position:
            self.connection.send_measurement("gear_lever_position", value)
            self.dynamics_model.gear_lever_position = value

    @property
    def headlamp_status(self):
        return self.headlamp

    @headlamp_status.setter
    def headlamp_status(self, value):
        if value != self.headlamp:
            self.connection.send_measurement("headlamp_status", value)
            self.headlamp = value

    @property
    def high_beam_status(self):
        return self.highbeam

    @high_beam_status.setter
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

    def send_all_loop(self):
        snapshot = self.dynamics_model.snapshot
        now = datetime.datetime.now()

        for signal in self.data:
            if signal['fast_update']:
                if snapshot[signal['name']] != signal['last_value']:
                    self.connection.send_measurement(signal['name'],
                        snapshot[signal['name']])
            elif now > signal['deadline']:
                self.connection.send_measurement(signal['name'],
                    snapshot[signal['name']])
                signal['deadline'] = now + signal['period']
        time.sleep(0.01)

    def send_loop_1Hz(self):
        self.connection.send_measurement("latitude",
                        self.dynamics_model.lat)
        self.connection.send_measurement("longitude",
                        self.dynamics_model.lon)
        self.connection.send_measurement("parking_brake_status",
                        self.dynamics_model.parking_brake_status)
        self.connection.send_measurement("brake_pedal_status",
                        self.dynamics_model.brake_pedal_status)
        self.connection.send_measurement("transmission_gear_position",
                        self.dynamics_model.transmission_gear_position)
        self.connection.send_measurement("ignition_status",
                        self.dynamics_model.ignition_status)
        self.connection.send_measurement("headlamp_status",
                        self.headlamp)
        self.connection.send_measurement("high_beam_status",
                        self.headlamp)
        self.connection.send_measurement("windshield_wiper_status",
                        self.wipers)
        self.connection.send_measurement("gear_lever_position",
                        self.dynamics_model.gear_lever_position)
        for door in self.door_status:
            self.connection.send_measurement("door_status", door, self.door_status[door])
        time.sleep(1.0)

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

    def received_messages(self):
        return self.connection.received_messages()
