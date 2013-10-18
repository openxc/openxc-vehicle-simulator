from .data_calc import DataCalc
from datetime import datetime
import math

class LatCalc(DataCalc):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 42.292834
        self.last_calc = datetime.now()
        #self.earth_radius_km = 6378.1
        self.earth_circumference_km = 40075.0
        self.km_per_deg = self.earth_circumference_km / 360.0
        self.name = 'latitude'

    # Any necessary data should be passed in
    def iterate(self, snapshot):
        vehicle_speed = snapshot['vehicle_speed']
        heading = snapshot['heading']
        
        current_time = datetime.now()
        time_delta = current_time - self.last_calc
        self.last_calc = current_time
        time_step = time_delta.seconds + (
                float(time_delta.microseconds) / 1000000)

        distance = time_step * (vehicle_speed / 3600)
        N_S_dist = distance * math.cos(heading)

#        old_lat = math.radians( self.data )
#        new_lat = math.asin( math.sin(old_lat)*math.cos(distance/self.earth_radius_km) +
#                            math.cos(old_lat)*math.sin(distance/self.earth_radius_km)*math.cos(heading))
        delta_lat = N_S_dist / self.km_per_deg

        self.data = self.data + delta_lat
        #Todo:  check for the poles
