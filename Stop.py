class Stop:

    def __init__(self, name):
        self.name = name
        self.schedules = dict() # a dict where the keys are bus_line_name and the values are others dicts where the
        # keys regular_go, regular_back and/or we_holidays_go, we_holidays_back and the value are the time for each
        # period
        self.neighbour_stop = []

    def add_bus_line_regular(self, bus_line_name, regular_date_go, regular_date_back):
        """ add the regular schedule of the new bus line"""

        if not(bus_line_name in self.schedules.keys()):
            self.schedules[bus_line_name] = dict()

        self.schedules[bus_line_name]["regular_go"] = regular_date_go[self.name]
        self.schedules[bus_line_name]["regular_back"] = regular_date_back[self.name]

    def add_bus_line_we_holidays(self, bus_line_name, we_holidays_date_go, we_holidays_date_back):
        """ add the we_holidays schedule of the new bus line"""

        if not(bus_line_name in self.schedules.keys()):
            self.schedules[bus_line_name] = dict()

        self.schedules[bus_line_name]["we_holidays_go"] = we_holidays_date_go[self.name]
        self.schedules[bus_line_name]["we_holidays_back"] = we_holidays_date_back[self.name],

    def add_neighbour_bus_stop(self, bus_stop):
        """ add the next bus stop"""
        self.neighbour_stop.append(bus_stop)