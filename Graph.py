from Stop import Stop

class Graph:  # composed of bus lines

    def __init__(self):
        self.stops = []

    def dates2dic(self, dates):
        dic = {}
        splitted_dates = dates.split("\n")
        # print(splitted_dates)
        for stop_dates in splitted_dates:
            tmp = stop_dates.split(" ")
            dic[tmp[0]] = tmp[1:]
        return dic

    def add_bus_line(self, filename):
        """ add a new bus line to the network
        :param filename: filename of the new bus line """

        # if there are new stops which aren't already in the stops list, it creates
        # them and add them to the list or if they are already there, it adds the new schedules of the bus line to
        # concerned stops

        try:
            with open(filename, 'r') as f:
                content = f.read()
        except OSError:
            # 'File not found' error message.
            print("File not found")

        slited_content = content.split("\n\n")
        regular_path = slited_content[0] # useless
        regular_date_go = self.dates2dic(slited_content[1])
        regular_date_back = self.dates2dic(slited_content[2])
        we_holidays_path = slited_content[3] # useless
        we_holidays_date_go = self.dates2dic(slited_content[4])
        we_holidays_date_back = self.dates2dic(slited_content[5])

        bus_line_name = filename[:len(filename) - 4]

        # NB: a Bus stop can be served on regular and/or on we_holidays date

        # regular_date
        for bus_stop_name in regular_date_go:
            bus_stop_names = [] # current list of stop names
            for bus_stop1 in self.stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus line to
                # the stop
                st = Stop(bus_stop_name)
                st.add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)
                self.stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                for bus_stop2 in self.stops: # search the stop in the list self.stops
                    if bus_stop2.name == bus_stop_name:
                        bus_stop2.add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)

        # we_holidays_date
        for bus_stop_name in we_holidays_date_go:  # in case that the lists of bus stop are not the same in regular and
            bus_stop_names = []
            for bus_stop1 in self.stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus line to
                # the stop
                st = Stop(bus_stop_name)
                st.add_bus_line_we_holidays(bus_line_name, we_holidays_date_go, we_holidays_date_back)
                self.stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                for bus_stop2 in self.stops:
                    if bus_stop2.name == bus_stop_name:
                        bus_stop2.add_bus_line_we_holidays(bus_line_name,  we_holidays_date_go, we_holidays_date_back)

    def shortest(self, start_stop, end_stop):
        pass

    def fastest(self, start_stop, end_stop):
        pass

    def foremost(self, start_stop, end_stop):
        pass
