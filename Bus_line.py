from Stop import Stop


class Bus_line:

    def __init__(self, name):
        self.name = name
        self.regular_stops = []
        self.holidays_stops = []

    def init_stop_regular(self, dict_stop_go, dict_stop_back):
        """ create each bus stop from a dict (dict_stop_go) and add it to self.regular_stops"""
        for stop in dict_stop_go:
            schedule_go = dict_stop_go[stop] #with dict, we reference to a specific element
            schedule_back = dict_stop_back[stop]
            self.regular_stops.append(Stop(stop, schedule_go, schedule_back))

    def init_stop_holidays(self, dict_stop_go, dict_stop_back): # regular_stops and holidays_stop might be different
        """ create each bus stop from a dict (dict_stop_go) and add it to self.holidays_stops"""
        for stop in dict_stop_go:
            schedule_go = dict_stop_go[stop] #with dict, we reference to a specific element
            schedule_back = dict_stop_back[stop]
            self.holidays_stops.append(Stop(stop, schedule_go, schedule_back))
