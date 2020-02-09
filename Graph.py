# By NoahRz

import math

from BusStop import BusStop


class Graph:

    def __init__(self):
        self.bus_stops = []  # list of BusStop

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
        regular_path = slited_content[0]
        regular_date_go = self.dates2dic(slited_content[1])
        regular_date_back = self.dates2dic(slited_content[2])
        we_holidays_path = slited_content[3]
        we_holidays_date_go = self.dates2dic(slited_content[4])
        we_holidays_date_back = self.dates2dic(slited_content[5])

        bus_line_name = filename[:len(filename) - 4]

        # NB: a Bus stop can be served on regular and/or on we_holidays date

        # we create regular_date bus_stop
        for bus_stop_name in regular_date_go:
            bus_stop_names = []  # current list of stop names
            for bus_stop1 in self.bus_stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus
                # line to the stop
                st = BusStop(bus_stop_name)
                st.add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)
                self.bus_stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                self.get_bus_stop(bus_stop_name).add_bus_line_regular(bus_line_name, regular_date_go, regular_date_back)

        # we create we_holidays_date bus_stop
        for bus_stop_name in we_holidays_date_go:  # in case that the lists of bus stop are not the same in regular and
            bus_stop_names = []
            for bus_stop1 in self.bus_stops:
                bus_stop_names.append(bus_stop1.name)

            if not (bus_stop_name in bus_stop_names):  # creates the new bus stop and adds the schedule of the bus
                # line to the stop
                st = BusStop(bus_stop_name)
                st.add_bus_line_we_holidays(bus_line_name, we_holidays_date_go, we_holidays_date_back)
                self.bus_stops.append(st)
            else:  # adds the new bus line if the bus stop is already in the network
                self.get_bus_stop(bus_stop_name).add_bus_line_we_holidays(bus_line_name, we_holidays_date_go,
                                                                          we_holidays_date_back)

        # add neighbour bus_stop for each bus_stop on regular_date (the regular and we_holidays paths might be
        # different)
        self.add_neighbour_bus_stops(regular_path)

        # add neighbour bus_stop for each bus_stop on we_holidays_date (the regular and we_holidays paths might be
        # different)
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

    def convert_time_to_min(self, time):
        """ return the converted time hour:min into min
        :param time: str
        :return int (minunte)"""
        return int(time.split(":")[0]) * 60 + int(time.split(":")[1])


    def fastest(self, bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked):  #  showing the path, just take the fastest path
        """ initialise dijkstra addapted to the problem and start the dijkstra's algorithm
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param time_asked : String, time asked by the user
        :param date_asked : String, date asked by the user "regular" or we_holidays"
        :return list of bus_stops served to get to bus_stop_end
        """
        # initialisation
        bus_stop_to_visit = []
        max_time = math.inf
        dist = {}  # ex {"bus_stop1_name": {"time_to_get_there":dist1, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop1, "bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1, "index":index1}, "bus_stop2_name": {"time_to_get_there":dist2, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop2,"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2, "index":index2},...}
        # last_bus_to_get_there : the time when the bus leave the previous bus_stop to arrive to the current bus_stop
        paths = {} # track the fastest path to get to each bus_stop
        # ex path =  {"bus_stop1_name":[{"bus_stop11_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time11}},{"bus_stop12_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time12}},...],
        #             "bus_stop2_name":[{"bus_stop21_name":{"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2,"time":time21}},{"bus_stop22_name":{"bus_line_name":bus_line_name2 "date_dir_asked": date_dir_asked1,"time":time22}},...]
        #             ,...}

        for bus_stop in bus_stops:
            bus_stop_to_visit.append(bus_stop)
            dist[bus_stop.name] = {"time_to_get_there": max_time,
                                   "last_bus_to_get_there": {"last_bus_stop": None, "bus_line_name": None, "date_dir_asked": None,
                                                             "index": None}}
            paths[bus_stop.name] = []

        dist[bus_stop_start.name]["time_to_get_there"] = 0  # set the time_to_get_there from bus_stop_start to itself to 0
        dist[bus_stop_start.name]["last_bus_to_get_there"] = {"last_bus_stop" : None, "bus_line": None, "date_dir_asked": None, "index": None}
        bus_stop_to_visit.remove(bus_stop_start)  # remove the bus_stop_start from bus to visit because we are already at this bus_stop
        return self.fastest_algorithm(bus_stops, bus_stop_start, bus_stop_end, bus_stop_start, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)

    def fastest_algorithm(self, bus_stops, bus_stop_start, bus_stop_end, bus_stop_current, time_asked, date_asked, bus_stop_to_visit, dist, paths):
        """
        do the dijkstra's algorthm and return the fastest path from bus_stop_star to bus_stop_end considering the time_asked and the date_asked
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param bus_stop_current: bus_stop where we are currently
        :param time_asked: String, time asked by the user
        :param date_asked:  String, date asked by the user "regular" or we_holidays"
        :param bus_stop_to_visit: list
        :param dist: dict of bus_stop giving for each bus_stop the distance(time) from the bus_stop_start to the bus_stop, the last_bus_stop served, the bus_line_name taken, the date and direction and the index of the time in the bus_stop schedules
        :param paths: dict of bus_stop giving for each bust_stop the path to get to the bus_stop from the bus_stop_start
        :return: list of bus_stop served to get to all the bus_stop of the network
        """

        if bus_stop_current == bus_stop_end: # we reach our goal by taking the fastest path
            return paths[bus_stop_end.name]

        for bus_stop_neighbour in bus_stop_current.get_bus_stop_neighbour():
            if bus_stop_neighbour in bus_stop_to_visit:

                for bus_line_name in self.bus_lines_shared(bus_stop_current, bus_stop_neighbour):  # two bus stops could
                    # share several bus lines, but we don't care if we arrive at the neighbour bus stop the fastest way
                    if bus_stop_neighbour in bus_stop_current.next_bus_stop:
                        date_dir_asked = date_asked + "_go"
                    else:
                        date_dir_asked = date_asked + "_back"

                    index = bus_stop_current.get_index_closest_time(bus_line_name, date_dir_asked,
                                                                    time_asked)  # index is the index of the closest time (in the bus_line_name) to time asked

                    while bus_stop_neighbour.get_time(bus_line_name, date_dir_asked,
                                                      index) == '-':
                        index = index + 1  # even if we are in the back direction we add 1 because the schedule is reversed (kinda)

                    waiting_time = self.convert_time_to_min(bus_stop_current.schedules[bus_line_name][date_dir_asked][index]) - self.convert_time_to_min(time_asked)
                    # waiting time before taking the bus
                    if waiting_time < 0:  # if we wait for the first bus tomorrow
                        waiting_time = (self.convert_time_to_min('24:00')-self.convert_time_to_min(time_asked)) + self.convert_time_to_min(bus_stop_current.schedules[bus_line_name][date_dir_asked][index])

                    time_bus_stop_neighbour = self.convert_time_to_min(bus_stop_neighbour.get_time(bus_line_name, date_dir_asked, index))
                    time_bus_stop_current = self.convert_time_to_min(bus_stop_current.get_time(bus_line_name, date_dir_asked, index))

                    weight = (time_bus_stop_neighbour - time_bus_stop_current) + waiting_time  # time (in minute) between these 2 bus stops

                    new_dist = weight + dist[bus_stop_current.name]["time_to_get_there"]
                    if new_dist < dist[bus_stop_neighbour.name]["time_to_get_there"]:
                        dist[bus_stop_neighbour.name]["time_to_get_there"] = new_dist
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["last_bus_stop"] = bus_stop_current
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["bus_line_name"] = bus_line_name
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["date_dir_asked"] = date_dir_asked
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["index"] = index

        # choose the closest bus_stop from the initial bus_stop
        min_time = math.inf
        bus_stop_closest_to_start_and_not_yet_visited = None
        for bus_stop in bus_stop_to_visit:
            if dist[bus_stop.name]["time_to_get_there"] <= min_time:
                min_time = dist[bus_stop.name]["time_to_get_there"]
                bus_stop_closest_to_start_and_not_yet_visited = bus_stop

        bus_stop_to_visit.remove(bus_stop_closest_to_start_and_not_yet_visited)

        bus_line_name1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["bus_line_name"]
        date_dir_asked1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["date_dir_asked"]
        index1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["index"]
        time_asked = bus_stop_closest_to_start_and_not_yet_visited.schedules[bus_line_name1][date_dir_asked1][index1]

        #track the path to get to the bus_stop_closest_to_start_and_not_yet_visited
        last_bus_stop1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["last_bus_stop"]


        time = last_bus_stop1.schedules[bus_line_name1][date_dir_asked1][index1]
        #time is the time when the bus is at the bus_stop


        paths[bus_stop_closest_to_start_and_not_yet_visited.name].extend(paths[last_bus_stop1.name]) # we add the path to get to the last bus_stop
        if paths[bus_stop_closest_to_start_and_not_yet_visited.name] == []: # In case that the path is empty, we add the first bus_stop from where we leave
            paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({last_bus_stop1.name:{"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time}})
        paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({bus_stop_closest_to_start_and_not_yet_visited.name: {"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time_asked}})
        # we add the next bus_stop we will serve

        return self.fastest_algorithm(bus_stops, bus_stop_start, bus_stop_end,
                                       bus_stop_closest_to_start_and_not_yet_visited, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)

    def shortest(self, bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked):  #  showing the path, just take the shortest path
        """ initialise dijkstra addapted to the problem and start the dijkstra's algorithm
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param time_asked : String, time asked by the user
        :param date_asked : String, date asked by the user "regular" or we_holidays"
        :return list of bus_stops served to get to bus_stop_end
        """
        # initialisation
        bus_stop_to_visit = []
        nb_max_step = math.inf
        dist = {}  # ex {"bus_stop1_name": {"step_nb":step1, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop1, "bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1, "index":index1}, "bus_stop2_name": {"step_nb":step2, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop2,"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2, "index":index2},...}
        # last_bus_to_get_there : the time when the bus leave the previous bus_stop to arrive to the current bus_stop
        paths = {} # track the fastest path to get to each bus_stop
        # ex path =  {"bus_stop1_name":[{"bus_stop11_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time11}},{"bus_stop12_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time12}},...],
        #             "bus_stop2_name":[{"bus_stop21_name":{"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2,"time":time21}},{"bus_stop22_name":{"bus_line_name":bus_line_name2 "date_dir_asked": date_dir_asked1,"time":time22}},...]
        #             ,...}

        for bus_stop in bus_stops:
            bus_stop_to_visit.append(bus_stop)
            dist[bus_stop.name] = {"step_nb": nb_max_step,
                                   "last_bus_to_get_there": {"last_bus_stop": None, "bus_line_name": None, "date_dir_asked": None,
                                                             "index": None}}
            paths[bus_stop.name] = []

        dist[bus_stop_start.name]["step_nb"] = 0  # set the nb_step from bus_stop_start to itself to 0
        dist[bus_stop_start.name]["last_bus_to_get_there"] = {"last_bus_stop" : None, "bus_line": None, "date_dir_asked": None, "index": None}
        bus_stop_to_visit.remove(bus_stop_start)  # remove the bus_stop_start from bus to visit because we are already at this bus_stop
        return self.shortest_algorithm(bus_stops, bus_stop_start, bus_stop_end, bus_stop_start, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)

    def shortest_algorithm(self, bus_stops, bus_stop_start, bus_stop_end, bus_stop_current, time_asked, date_asked, bus_stop_to_visit, dist, paths):
        """
        do the dijkstra's algorthm and return the shortest path from bus_stop_star to bus_stop_end considering the time_asked and the date_asked
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param bus_stop_current: bus_stop where we are currently
        :param time_asked: String, time asked by the user
        :param date_asked:  String, date asked by the user "regular" or we_holidays"
        :param bus_stop_to_visit: list
        :param dist: dict of bus_stop giving for each bus_stop the distance(time) from the bus_stop_start to the bus_stop, the last_bus_stop served, the bus_line_name taken, the date and direction and the index of the time in the bus_stop schedules
        :param paths: dict of bus_stop giving for each bust_stop the path to get to the bus_stop from the bus_stop_start
        :return: list of bus_stop served to get to all the bus_stop of the network
        """
        if bus_stop_current == bus_stop_end: #  we reach our goal by taking the shortest path
            return paths[bus_stop_end.name]

        for bus_stop_neighbour in bus_stop_current.get_bus_stop_neighbour():
            if bus_stop_neighbour in bus_stop_to_visit:

                for bus_line_name in self.bus_lines_shared(bus_stop_current, bus_stop_neighbour):  # two bus stops could
                    # share several bus lines, but we don't care if we arrive at the neighbour bus stop the fastest way
                    if bus_stop_neighbour in bus_stop_current.next_bus_stop:
                        date_dir_asked = date_asked + "_go"
                    else:
                        date_dir_asked = date_asked + "_back"

                    index = bus_stop_current.get_index_closest_time(bus_line_name, date_dir_asked,
                                                                    time_asked)  # index is the index of the closest time (in the bus_line_name) to time asked

                    while bus_stop_neighbour.get_time(bus_line_name, date_dir_asked,
                                                      index) == '-':
                        index = index + 1  # even if we are in the back direction we add 1 because the schedule is reversed (kinda)

                    new_dist = 1 + dist[bus_stop_current.name]["step_nb"]
                    if new_dist < dist[bus_stop_neighbour.name]["step_nb"]:
                        dist[bus_stop_neighbour.name]["step_nb"] = new_dist
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["last_bus_stop"] = bus_stop_current
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["bus_line_name"] = bus_line_name
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["date_dir_asked"] = date_dir_asked
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["index"] = index

        # choose the closest bus_stop from the initial bus_stop
        min_nb_step = math.inf
        bus_stop_closest_to_start_and_not_yet_visited = None
        for bus_stop in bus_stop_to_visit:
            if dist[bus_stop.name]["step_nb"] <= min_nb_step:
                min_nb_step = dist[bus_stop.name]["step_nb"]
                bus_stop_closest_to_start_and_not_yet_visited = bus_stop

        bus_stop_to_visit.remove(bus_stop_closest_to_start_and_not_yet_visited)

        bus_line_name1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["bus_line_name"]
        date_dir_asked1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["date_dir_asked"]
        index1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["index"]
        time_asked = bus_stop_closest_to_start_and_not_yet_visited.schedules[bus_line_name1][date_dir_asked1][index1]

        #track the path to get to the bus_stop_closest_to_start_and_not_yet_visited
        last_bus_stop1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["last_bus_stop"]


        time = last_bus_stop1.schedules[bus_line_name1][date_dir_asked1][index1]
        #time is the time when the bus is at the bus_stop


        paths[bus_stop_closest_to_start_and_not_yet_visited.name].extend(paths[last_bus_stop1.name]) # we add the path to get to the last bus_stop
        if paths[bus_stop_closest_to_start_and_not_yet_visited.name] == []: # In case that the path is empty, we add the first bus_stop from where we leave
            paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({last_bus_stop1.name:{"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time}})
        paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({bus_stop_closest_to_start_and_not_yet_visited.name: {"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time_asked}})
        # we add the next bus_stop we will serve

        return self.shortest_algorithm(bus_stops, bus_stop_start, bus_stop_end,
                                       bus_stop_closest_to_start_and_not_yet_visited, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)

    def foremost(self, bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked):  #  showing the path, just take the Foremost path
        """ initialise dijkstra addapted to the problem and start the dijkstra's algorithm
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param time_asked : String, time asked by the user
        :param date_asked : String, date asked by the user "regular" or we_holidays"
        :return list of bus_stops served to get to bus_stop_end
        """
        # initialisation
        bus_stop_to_visit = []
        max_time_arrived = math.inf
        dist = {}  # ex {"bus_stop1_name": {"time_arrived":time_arrived1, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop1, "bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1, "index":index1}, "bus_stop2_name": {"time_arrived":time_arrived2, "last_bus_to_get_there":{"last_bus_stop_name": last_bus_stop2,"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2, "index":index2},...}
        # last_bus_to_get_there : the time when the bus leave the previous bus_stop to arrive to the current bus_stop
        paths = {} # track the fastest path to get to each bus_stop
        # ex path =  {"bus_stop1_name":[{"bus_stop11_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time11}},{"bus_stop12_name":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1,"time":time12}},...],
        #             "bus_stop2_name":[{"bus_stop21_name":{"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2,"time":time21}},{"bus_stop22_name":{"bus_line_name":bus_line_name2 "date_dir_asked": date_dir_asked1,"time":time22}},...]
        #             ,...}

        for bus_stop in bus_stops:
            bus_stop_to_visit.append(bus_stop)
            dist[bus_stop.name] = {"time_arrived": max_time_arrived,
                                   "last_bus_to_get_there": {"last_bus_stop": None, "bus_line_name": None, "date_dir_asked": None,
                                                             "index": None}}
            paths[bus_stop.name] = []

        dist[bus_stop_start.name]["time_arrived"] = 0  # set the distance from bus_stop_start to itself to 0
        dist[bus_stop_start.name]["last_bus_to_get_there"] = {"last_bus_stop" : None, "bus_line": None, "date_dir_asked": None, "index": None}
        bus_stop_to_visit.remove(bus_stop_start)  # remove the bus_stop_start from bus to visit because we are already at this bus_stop
        return self.foremost_algorithm(bus_stops, bus_stop_start, bus_stop_end, bus_stop_start, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)

    def foremost_algorithm(self, bus_stops, bus_stop_start, bus_stop_end, bus_stop_current, time_asked, date_asked, bus_stop_to_visit, dist, paths):
        """
        do the dijkstra's algorthm and return the fastest path from bus_stop_star to bus_stop_end considering the time_asked and the date_asked
        :param bus_stops: list of all the bus_stop
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_end: bus_stop where we want to go
        :param bus_stop_current: bus_stop where we are currently
        :param time_asked: String, time asked by the user
        :param date_asked:  String, date asked by the user "regular" or we_holidays"
        :param bus_stop_to_visit: list
        :param dist: dict of bus_stop giving for each bus_stop the distance(time) from the bus_stop_start to the bus_stop, the last_bus_stop served, the bus_line_name taken, the date and direction and the index of the time in the bus_stop schedules
        :param paths: dict of bus_stop giving for each bust_stop the path to get to the bus_stop from the bus_stop_start
        :return: list of bus_stop served to get to all the bus_stop of the network
        """
        if bus_stop_current == bus_stop_end: #  we reach our goal by taking the foremost path
            return paths[bus_stop_end.name]

        for bus_stop_neighbour in bus_stop_current.get_bus_stop_neighbour():
            if bus_stop_neighbour in bus_stop_to_visit:

                for bus_line_name in self.bus_lines_shared(bus_stop_current, bus_stop_neighbour):  # two bus stops could
                    # share several bus lines, but we don't care if we arrive at the neighbour bus stop the fastest way
                    if bus_stop_neighbour in bus_stop_current.next_bus_stop:
                        date_dir_asked = date_asked + "_go"
                    else:
                        date_dir_asked = date_asked + "_back"

                    index = bus_stop_current.get_index_closest_time(bus_line_name, date_dir_asked,
                                                                    time_asked)  # index is the index of the closest time (in the bus_line_name) to time asked

                    while bus_stop_neighbour.get_time(bus_line_name, date_dir_asked,
                                                      index) == '-':
                        index = index + 1  # even if we are in the back direction we add 1 because the schedule is reversed (kinda)

                    waiting_time = self.convert_time_to_min(bus_stop_current.schedules[bus_line_name][date_dir_asked][index]) - self.convert_time_to_min(time_asked)
                    # waiting time before taking the bus (works)
                    time_arrived_at_bus_stop_neighbour = self.convert_time_to_min(bus_stop_neighbour.get_time(bus_line_name, date_dir_asked, index))
                    if waiting_time < 0:  # if we wait for the first bus tomorrow
                        time_arrived_at_bus_stop_neighbour = time_arrived_at_bus_stop_neighbour + (60*24)
                        # we add one day, don't really matter the additional value (it might be different than the real
                        # waiting time) but it has to be enough greater to recognize that we wait for the next day

                    if time_arrived_at_bus_stop_neighbour < dist[bus_stop_neighbour.name]["time_arrived"]:
                        dist[bus_stop_neighbour.name]["time_arrived"] = time_arrived_at_bus_stop_neighbour
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["last_bus_stop"] = bus_stop_current
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["bus_line_name"] = bus_line_name
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["date_dir_asked"] = date_dir_asked
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["index"] = index

        # choose the closest bus_stop from the initial bus_stop
        min_time = math.inf
        bus_stop_closest_to_start_and_not_yet_visited = None
        for bus_stop in bus_stop_to_visit:
            if dist[bus_stop.name]["time_arrived"] <= min_time:
                min_time = dist[bus_stop.name]["time_arrived"]
                bus_stop_closest_to_start_and_not_yet_visited = bus_stop

        bus_stop_to_visit.remove(bus_stop_closest_to_start_and_not_yet_visited)

        bus_line_name1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["bus_line_name"]
        date_dir_asked1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["date_dir_asked"]
        index1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["index"]
        time_asked = bus_stop_closest_to_start_and_not_yet_visited.schedules[bus_line_name1][date_dir_asked1][index1]

        #track the path to get to the bus_stop_closest_to_start_and_not_yet_visited
        last_bus_stop1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["last_bus_stop"]

        time = last_bus_stop1.schedules[bus_line_name1][date_dir_asked1][index1]
        #time is the time when the bus is at the bus_stop

        paths[bus_stop_closest_to_start_and_not_yet_visited.name].extend(paths[last_bus_stop1.name]) # we add the path to get to the last bus_stop
        if paths[bus_stop_closest_to_start_and_not_yet_visited.name] == []: # In case that the path is empty, we add the first bus_stop from where we leave
            paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({last_bus_stop1.name:{"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time}})
        paths[bus_stop_closest_to_start_and_not_yet_visited.name].append({bus_stop_closest_to_start_and_not_yet_visited.name: {"bus_line_name": bus_line_name1, "date_dir_asked": date_dir_asked1, "Time": time_asked}})
        # we add the next bus_stop we will serve

        return self.foremost_algorithm(bus_stops, bus_stop_start, bus_stop_end,
                                       bus_stop_closest_to_start_and_not_yet_visited, time_asked, date_asked,
                                       bus_stop_to_visit, dist, paths)


    def bus_lines_shared(self, bus_stop1, bus_stop2):
        """ return a list of all the bus line shared by two bus_stop"""
        bus_lines_shared = []  # list of names of each bus line
        for bus_line_name in bus_stop1.schedules:  # if they have one shared bus_line, it has to be in bus_stop1's bus lines (we could do it with bus_stop2)
            if bus_line_name in bus_stop2.schedules:
                bus_lines_shared.append(bus_line_name)
        return bus_lines_shared




