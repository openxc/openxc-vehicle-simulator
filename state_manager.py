import enabler_connection
import dynamics_model
import threading
import time
import datetime
import math

class StateManager(object):
    def __init__(self):
        self.stopped = False
        self.connection = enabler_connection.EnablerConnection()
        self.dynamics_model = dynamics_model.DynamicsModel()
        
        self.headlamp = False
        self.highbeams = False
        self.wipers = False
        self.door_status = {'driver':False, 'passenger':False,
                'left_rear':False, 'right_rear':False}

        self.start_send_loop(self.send_local_loop, "Send-Local-Thread")

        self.data = []
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'steering_wheel_angle',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.1,
                           'rounding': 1})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'torque_at_transmission',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.1,
                           'rounding': 1})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'engine_speed',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.1,
                           'rounding': 1})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'vehicle_speed',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.01,
                           'rounding': 2})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'accelerator_pedal_position',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.1,
                           'rounding': 1})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'parking_brake_status',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': True,
                           'last_value': False,
                           'precision': 0})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'brake_pedal_status',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': True,
                           'last_value': False,
                           'precision': 0})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'transmission_gear_position',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': True,
                           'last_value': 'first',
                           'precision': 0})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'gear_lever_position',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': True,
                           'last_value': 'drive',
                           'precision': 0})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'odometer',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.002,
                           'rounding': 3})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'ignition_status',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': True,
                           'last_value': 'run',
                           'precision': 0})
        period = datetime.timedelta(microseconds = 1000000/2)  #2Hz
        self.data.append({'name':'fuel_level',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 1,
                           'rounding': 0})
        period = datetime.timedelta(microseconds = 1000000/10)  #10Hz
        self.data.append({'name':'fuel_consumed_since_restart',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.000001,
                           'rounding': 6})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'latitude',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.00001,
                           'rounding': 5})
        period = datetime.timedelta(microseconds = 1000000/1)  #1Hz
        self.data.append({'name':'longitude',
                           'period': period,
                           'deadline': datetime.datetime.now() + period,
                           'fast_update': False,
                           'precision': 0.00001,
                           'rounding': 5})

        self.start_send_loop(self.send_dynamics_loop, "Send-Dynamic-Thread")

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
        self.dynamics_model.parking_brake_status = value

    @property
    def manual_trans_status(self):
        return self.dynamics_model.manual_trans_status

    @manual_trans_status.setter
    def manual_trans_status(self, value):
        self.dynamics_model.manual_trans_status = value

    @property
    def brake_pedal_position(self):
        return self.dynamics_model.brake

    @brake_pedal_position.setter
    def brake_pedal_position(self, value):
        self.dynamics_model.brake = value

    @property
    def ignition_status(self):
        return self.dynamics_model.ignition_status

    @ignition_status.setter
    def ignition_status(self, value):
        self.dynamics_model.ignition_status = value

    @property
    def gear_lever_position(self):
        return self.dynamics_model.gear_lever_position

    @gear_lever_position.setter
    def gear_lever_position(self, value):
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
        return self.highbeams

    @high_beam_status.setter
    def high_beam_status(self, value):
        if value != self.highbeams:
            self.connection.send_measurement("high_beam_status", value)
            self.highbeams = value

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

    @property
    def latitude(self):
        return self.dynamics_model.snapshot['latitude']

    @latitude.setter
    def latitude(self, value):
        self.dynamics_model.latitude = value

    @property
    def longitude(self):
        return self.dynamics_model.snapshot['longitude']

    @longitude.setter
    def longitude(self, value):
        self.dynamics_model.longitude = value

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

    def update_signal(self, signal, snapshot):
        value = snapshot[signal['name']]
        if signal['fast_update']:
                    signal['last_value'] = value

        if signal['precision'] != 0:
            value = value - (value % signal['precision'])
            value = round(value, signal['rounding'])

        self.connection.send_measurement(signal['name'],value)

    def send_dynamics_loop(self):
        snapshot = self.dynamics_model.snapshot
        now = datetime.datetime.now()

        for signal in self.data:
            if now > signal['deadline']:
                self.update_signal(signal, snapshot)
                signal['deadline'] = now + signal['period']                
            elif signal['fast_update']:
                if snapshot[signal['name']] != signal['last_value']:
                    self.update_signal(signal, snapshot)
        time.sleep(0.01)

    def send_local_loop(self):
        self.connection.send_measurement("headlamp_status",
                        self.headlamp)
        self.connection.send_measurement("high_beam_status",
                        self.highbeams)
        self.connection.send_measurement("windshield_wiper_status",
                        self.wipers)
        for door in self.door_status:
            self.connection.send_measurement("door_status", door, self.door_status[door])
        time.sleep(1.0)

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

    def upshift(self):
        self.dynamics_model.upshift();

    def downshift(self):
        self.dynamics_model.downshift();
