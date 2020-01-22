from Stop import Stop


class Bus_line:

    def __init__(self, name):
        self.name = name
        self.stops_regular = []
        self.stops_holidays = []

    def init_stop_regular(self, dict_stop_go, dict_stop_back):
        """ create each bus stop from a dict (dict_stop_go) and add it to self.stops_regular"""
        for stop in dict_stop_go:
            schedule_go = dict_stop_go[stop] #with dict, we reference to a specific element
            schedule_back = dict_stop_back[stop]
            self.stops_regular.append(Stop(stop, schedule_go, schedule_back))