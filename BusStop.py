# By NoahRz

class BusStop:

    def __init__(self, name):
        self.name = name
        self.schedules = dict()  # a dict where the keys are bus_line_name and the values are others dicts where the
        # keys regular_go, regular_back and/or we_holidays_go, we_holidays_back and the value are the time for each
        # period. Ex:
        # {"bus_line_name":{"regular_go":[...],"regular_back":[...],..,"we_holidays_back":[]},"bus_line_name_1":{..},..}
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

    def convert_time_to_min(self, time):
        """ return the converted time hour:min to min
        :param time: str
        :return int (minute)
        """
        return int(time.split(":")[0]) * 60 + int(time.split(":")[1])

    def get_bus_stop_neighbour(self):
        """return list : its bus stop neigbhours"""
        neighbours = []
        neighbours.extend(self.next_bus_stop)
        neighbours.extend(self.prev_bus_stop)
        return neighbours

    def get_time(self, bus_line_name, date_asked, index):
        """ return the time in bus_line_name, in date_asked at index
         :param bus_line_name : String
         :param date_asked: String, regular_go, regular_back, we_holidays_go, we_holidays_back
         :return String
         """
        return self.schedules[bus_line_name][date_asked][index]


    def get_index_closest_time(self, bus_line_name, date_dir_asked, time_asked):
        """ return the closest time to time_asked
        :param bus_line_name: String
        :param date_dir_asked: String ex "regular_go"
        :param time_asked : String
        """
        nb = (len(self.schedules[bus_line_name][date_dir_asked]))
        converted_time_asked = self.convert_time_to_min(time_asked) # convert the time_asked into minute

        for index in range(nb-1):
            # there are only 3 cases to return the right index, but for these three we return the index of the closest time
            # after (or equal) the time asked

            if self.schedules[bus_line_name][date_dir_asked][index] != "-":
                current_time = self.convert_time_to_min(self.schedules[bus_line_name][date_dir_asked][index])  # convert the current time to min
            else:
                current_time = None
            if self.schedules[bus_line_name][date_dir_asked][index + 1] != "-":
                next_time = self.convert_time_to_min(self.schedules[bus_line_name][date_dir_asked][index + 1])  # convert the next time to min
            else:
                next_time = None
            if self.schedules[bus_line_name][date_dir_asked][index] != "-" and self.schedules[bus_line_name][date_dir_asked][index + 1] != "-" and current_time == converted_time_asked:
                return index
            if self.schedules[bus_line_name][date_dir_asked][index] != "-" and self.schedules[bus_line_name][date_dir_asked][index + 1] != "-" and current_time < converted_time_asked < next_time:
                return index + 1
            if self.schedules[bus_line_name][date_dir_asked][index] == "-" and self.schedules[bus_line_name][date_dir_asked][index+1] != "-" and converted_time_asked < next_time:
                return index + 1

        # if we end up here, that means that we did not find a bus today, so we have to wait for the first one tomorrow
        for index in range(nb-1):
            if self.schedules[bus_line_name][date_dir_asked][index] != "-":
                return index
