class DataCalc(object):
    def __init__(self):
        self.initialize_data()

    def initialize_data(self):
        self.data = 0
        self.name = 'data'

    def get(self):
        return self.data

    def put(self, new_value):
        self.data = new_value

    def iterate(self, data):  # Any necessary data should be passed in
        pass

