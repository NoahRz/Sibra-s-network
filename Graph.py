from Stop import Stop


class Graph:  # composed of bus lines

    def __init__(self):
        self.bus_stops = []

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
        regular_path = slited_content[0]  # useless
        regular_date_go = self.dates2dic(slited_content[1])
        regular_date_back = self.dates2dic(slited_content[2])
        we_holidays_path = slited_content[3]  # useless
        we_holidays_date_go = self.dates2dic(slited_content[4])
        we_holidays_date_back = self.dates2dic(slited_content[5])

        bus_line_name = filename[:len(filename) - 4]

        # NB: a Bus stop can be served on regular and/or on we_holidays date

        # we create regular_date bus_stop
        for bus_stop_name in regular_date_go:  # TO OPTIMISE $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            bus_stop_names = []  # current list of stop names
            for bus_stop1 in self.bus_stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus
                # line to the stop
                st = Stop(bus_stop_name)
                st.add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)
                self.bus_stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                self.get_bus_stop(bus_stop_name).add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)

        # we create we_holidays_date bus_stop # TO OPTIMISE  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        for bus_stop_name in we_holidays_date_go:  # in case that the lists of bus stop are not the same in regular and
            bus_stop_names = []
            for bus_stop1 in self.bus_stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus
                # line to the stop
                st = Stop(bus_stop_name)
                st.add_bus_line_we_holidays(bus_line_name, we_holidays_date_go, we_holidays_date_back)
                self.bus_stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                self.get_bus_stop(bus_stop_name).add_bus_line_we_holidays(bus_line_name, we_holidays_date_go,
                                                                          we_holidays_date_back)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # add neighbour bus_stop for each bus_stop on regular_date (the regular and we_holidays paths might be
        # differents)
        self.add_neighbour_bus_stops(regular_path)

        # add neighbour bus_stop for each bus_stop on we_holidays_date (the regular and we_holidays paths might be
        # differents)
        self.add_neighbour_bus_stops(we_holidays_path)

    def get_bus_stop(self, bus_stop_name):
        """ return the bus_stop named bus_stop_name"""
        for bus_stop in self.bus_stops:
            if bus_stop.name == bus_stop_name:
                return bus_stop

    def add_neighbour_bus_stops(self, path):
        """ add the neighbour bus stops to each each bus stop on the path (create the path)
        :param path: string """

        split_path = path.split(" ")  # we create a split list from a string
        for bus_stop_name in split_path:
            if bus_stop_name != "+" and bus_stop_name != "N":
                i = split_path.index(bus_stop_name)
                while i < (len(split_path) - 1) and split_path[i] != "N":
                    i = i + 1
                if i <= len(split_path) - 2:
                    bus_stop1 = self.get_bus_stop(bus_stop_name)
                    bus_stop2 = self.get_bus_stop(split_path[i + 1])
                    if bus_stop2 not in bus_stop1.next_bus_stop:  # to avoid duplication
                        bus_stop1.add_next_bus_stop(bus_stop2)
                    if bus_stop1 not in bus_stop2.prev_bus_stop:
                        bus_stop2.add_prev_bus_stop(bus_stop1)

    def find_path1(self, bus_stop_start, bus_stop_end, time_asked, date_asked):
        """ return the first path found from
        :param bus_stop_start : Stop obj
        :param bus_stop_end : Stop obj
        :param time_asked: time asked by the user
        :param date_asked: "regular" or "we_holidays" aked by the user
        :return list of the bus stops on the path from bus_stop_star to bus_stop_end"""
        # bus_stops_to_visit = []
        # for bus_stop in self.bus_stops:
        #     bus_stops_to_visit.append(bus_stop)
        #
        # bus_stops_to_visit.remove(bus_stop_start)
        #
        # bus_stop_current = bus_stop_start
        # while bus_stop_current != bus_stop_end:
        # for bus_stop in bus_stop_current.neighbour_bus_stop:

        #departure_time = bus_stop_start.get_closest_time(time_asked, date_asked)

        # path = []
        # #path = [{"from_bus_stop_name":bus_stop_start.name, "to_bus_stop_name" : "a", "bus_line_name": departure_time["bus_line_name"], "Departure_time": departure_time["closest_time"]}]
        # bus_stop_current = bus_stop_start
        # bus_stop_current_neighbour = []
        # bus_stop_current_neighbour.extend(bus_stop_current.next_bus_stop)
        # bus_stop_current_neighbour.extend(bus_stop_current.prev_bus_stop)
        #
        # while bus_stop_current != bus_stop_end:
        #     for bus_stop_neighbour in bus_stop_current_neighbour:
        #         if bus_stop_neighbour in bus_stop_current.next_bus_stop: # next bus stop
        #             date_path = date_asked +"_go" # ex date_path = "regular_go" or "we_holidays_go"
        #             closest_time = bus_stop_current.get_closest_time(time_asked, date_path)
        #             arrival_time = bus_stop_neighbour.schedules[closest_time["bus_line_name"]][date_path][closest_time["index"]]
        #             arrival_time_min = self.convert_time_in_min(arrival_time)
        #             departure_time = closest_time["closest_time"]
        #             departure_time_min = self.convert_time_in_min(departure_time)
        #             if arrival_time_min >= departure_time_min:
        #                 step = {"from_bus_stop_name": bus_stop_current.name,
        #                         "to_bus_stop_name": bus_stop_neighbour,
        #                         "bus_line_name": closest_time["bus_line_name"],
        #                         "Departure_time": departure_time,
        #                         "Arrival_time": arrival_time}
        #                 path.append(step)
        #                 path.append(self.find_path(bus_stop_neighbour, bus_stop_end, arrival_time, date_asked))
        #
        #         else:
        #             date_path = date_asked + "_back"  # ex date_path = "regular_back" or "we_holidays_back"
        #             closest_time = bus_stop_current.get_closest_time(time_asked, date_path)
        #             arrival_time = bus_stop_neighbour.schedules[closest_time["bus_line_name"]][date_path][closest_time["index"]]
        #             arrival_time_min = self.convert_time_in_min(arrival_time)
        #             departure_time = closest_time["closest_time"]
        #             departure_time_min = self.convert_time_in_min(departure_time)
        #             if arrival_time_min >= departure_time_min:
        #                 step = {"from_bus_stop_name": bus_stop_current.name,
        #                         "to_bus_stop_name": bus_stop_neighbour,
        #                         "bus_line_name": closest_time["bus_line_name"],
        #                         "Departure_time": departure_time,
        #                         "Arrival_time": arrival_time}
        #                 path.append(step)
        #                 path.append(self.find_path(bus_stop_neighbour, bus_stop_end,arrival_time, date_asked))

            # for bus_stop_neighbour in bus_stop_current.neighbour_bus_stop:
            #     closest_time = bus_stop_current.get_closest_time(time_asked, date_asked)
            #     if bus_stop_neighbour.convert_in_time(bus_stop_neighbour.schedules[closest_time["bus_line_name"]][closest_time["index"]])>closest_time["closest_time"]:
            #         path.append({"from_bus_stop_name":bus_stop_current.name, "to_bus_stop_name" : bus_stop_neighbour.name, "bus_line_name": closest_time["bus_line_name"], "Departure_time": bus_stop_neighbour.schedules[closest_time["bus_line_name"]][closest_time["index"]]})
            #         bus_stop_current=bus_stop_neighbour

                # if bus_stop_neighbour.convert_in_time(bus_stop_neighbour.schedules[departure_time["bus_line_name"]][departure_time["index"]]) > departure_time:
                #     departure_time = {"bus_stop_name":bus_stop_neighbour.name,"bus_line": departure_time["bus_line_name"], "closest_time": bus_stop_neighbour.schedules[departure_time["bus_line_name"]][departure_time["index"]]}
                #     path.append(bus_stop_neighbour)
                #     bus_stop_current = bus_stop_neighbour
        # return path

    def find_path(self,  bus_stop_start, bus_stop_end, time):
        # """ find the path between bus_stop_start and bus_stop_end, direction : go"""
        # path = [bus_stop_start]
        # bus_stop_current = bus_stop_start
        # while bus_stop_current is not bus_stop_end:
        #     neighbours = []
        #     neighbours.extend(bus_stop_current.next_bus_stop)
        #     #neighbours.extend(bus_stop_current.prev_bus_stop)
        #     for bus_stop_neighbour in neighbours:
        #         if bus_stop_neighbour != None:
        #             path.append(bus_stop_current)
        #             bus_stop_current = bus_stop_neighbour
        # path.append(bus_stop_current)
        # return path
        pass

    def find_path_new(self, bus_stop_star, bus_stop_end, path=[]):

        # if self.on_same_bus_line(bus_stop_star, bus_stop_end): # IT WORKS, TO SHOW ONE DIRECTION IN THE SAME BUS LINE
        #     bus_stop_current = bus_stop_star
        #     path.append(bus_stop_current)
        #     while bus_stop_current != bus_stop_end:
        #         for bus_stop_neighbour in bus_stop_current.next_bus_stop:
        #             if not (bus_stop_neighbour in path):
        #                 return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
        #     return path


        # bus_stop_current = bus_stop_star
        # path.append(bus_stop_current)
        # while bus_stop_current != bus_stop_end:
        #     if bus_stop_current.has_next_bus_stop(): # do not know if it's useful
        #         for bus_stop_neighbour in bus_stop_current.next_bus_stop:
        #             if not (bus_stop_neighbour in path):
        #                          return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
        #     if bus_stop_current.has_prev_bus_stop(): # do not know if it's useful
        #         for bus_stop_neighbour in bus_stop_current.prev_bus_stop:
        #             if not (bus_stop_neighbour in path):
        #             return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
        #
        #     return path
        # return path

        bus_stop_current = bus_stop_star
        path.append(bus_stop_current)
        while bus_stop_current != bus_stop_end:
            if bus_stop_current.has_next_bus_stop():  # do not know if it's useful
                for bus_stop_neighbour in bus_stop_current.next_bus_stop:
                    if not (bus_stop_neighbour in path):
                        return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
            if bus_stop_current.has_prev_bus_stop():  # do not know if it's useful
                for bus_stop_neighbour in bus_stop_current.prev_bus_stop:
                    # if not (bus_stop_neighbour in path):
                        return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
            return path
        return path

        # bus_stop_current = bus_stop_star
        # path.append(bus_stop_current)
        # while bus_stop_current != bus_stop_end:
        #     if bus_stop_current.has_next_bus_stop() or bus_stop_current.has_prev_bus_stop() : # do not know if it's useful
        #         neighbours = []
        #         neighbours.extend(bus_stop_current.next_bus_stop)
        #         neighbours.extend(bus_stop_current.prev_bus_stop)
        #         for bus_stop_neighbour in neighbours:
        #             if not (bus_stop_neighbour in path):
        #                          return self.find_path_new(bus_stop_neighbour, bus_stop_end, path)
        #     return path
        # return path


    def convert_time_in_min(self, time):
        """ return the converted time hour:min into min
        :param time: str
        :return int (minunte)"""
        return int(time.split(":")[0]) * 60 + int(time.split(":")[1])

    def test_fastest(self, bus_stops, bus_stop_start, bus_stop_end): # like dijkstra
        """ return the fatest path from bus_stop_start to bus_stop_end"""
    
    def shortest(self, start_stop, end_stop):
        pass

    def fastest(self, start_stop, end_stop):
        pass

    def foremost(self, start_stop, end_stop):
        pass

    def on_same_bus_line(self, bus_stop1, bus_stop2):
        """return True if bus_stop1 and bus_stop2 are on the same bus line, else False"""
        for bus_line_name in bus_stop1.schedules: # if they have one shared bus_line, it has to be in bus_stop1's bus lines (we could do it with bus_stop2)
            if bus_line_name in bus_stop2.schedules:
                return True
        return False

        pass
