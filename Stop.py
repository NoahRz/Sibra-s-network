class Stop:

    def __init__(self, name):
        self.name = name
        self.schedules = dict()  # a dict where the keys are bus_line_name and the values are others dicts where the
        # keys regular_go, regular_back and/or we_holidays_go, we_holidays_back and the value are the time for each
        # period
        self.next_bus_stop = []  # bus stop after self in path go, we create these to know which schedule use (go or back)
        self.prev_bus_stop = []  # bus stop after self in path back

    def add_bus_line_regular(self, bus_line_name, regular_date_go, regular_date_back):
        """ add the regular schedule of the new bus line"""

        if not (bus_line_name in self.schedules.keys()):
            self.schedules[bus_line_name] = dict()

        self.schedules[bus_line_name]["regular_go"] = regular_date_go[self.name]
        self.schedules[bus_line_name]["regular_back"] = regular_date_back[self.name]

    def add_bus_line_we_holidays(self, bus_line_name, we_holidays_date_go, we_holidays_date_back):
        """ add the we_holidays schedule of the new bus line"""

        if not (bus_line_name in self.schedules.keys()):
            self.schedules[bus_line_name] = dict()

        self.schedules[bus_line_name]["we_holidays_go"] = we_holidays_date_go[self.name]
        self.schedules[bus_line_name]["we_holidays_back"] = we_holidays_date_back[self.name]

    def add_next_bus_stop(self, bus_stop):
        """ add the next bus stop"""
        self.next_bus_stop.append(bus_stop)

    def add_prev_bus_stop(self, bus_stop):
        """ add the previous bus stop"""
        self.prev_bus_stop.append(bus_stop)

    def convert_time_in_min(self, time):  # Warning same function in Graph class
        """ return the converted time hour:min into min
        :param time: str
        :return int (minunte)"""
        return int(time.split(":")[0]) * 60 + int(time.split(":")[1])

    def get_closest_time(self, time_asked, date_path):
        """ return the closest time in schedules to time_asked
        :return dict {"bus_line" : bus_line_name, "date_asked":date_asked, "index":index}"""
        convert_time_asked_in_min = self.convert_time_in_min(time_asked)

        for bus_line_name in self.schedules:
            index = 0
            while index < len(self.schedules[bus_line_name][date_path][
                                  index]) and convert_time_asked_in_min <= self.convert_time_in_min(
                    self.schedules[bus_line_name][date_path][index]):
                index = index + 1
            return {"bus_line_name": bus_line_name, "closest_time": self.schedules[bus_line_name][date_path][index],
                    "index": index}

    def has_prev_bus_stop(self):
        """return True if this bus stop has prev_bus_stop, else False"""
        return self.prev_bus_stop != []

    def has_next_bus_stop(self):
        """return True if this bus stop has next_bus_stop, else False"""
        return self.next_bus_stop != []
