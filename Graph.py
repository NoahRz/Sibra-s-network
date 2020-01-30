import datetime
import math

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
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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


    def find_path_new(self, bus_stop_star, bus_stop_end, path=[]):

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

    def convert_time_in_min(self, time):
        """ return the converted time hour:min into min
        :param time: str
        :return int (minunte)"""
        return int(time.split(":")[0]) * 60 + int(time.split(":")[1])

    def test_fastest(self, bus_stops, bus_stop_start, bus_stop_current,  bus_stop_end, time_asked, date_asked, fastest_distance = {}, visited_bus_stop = [], predecessor = {}, path = []):  # like dijkstra
        """ return the fatest path from bus_stop_start to bus_stop_end
        :param bus_stops: list of all the bus_stops of the network
        :param bus_stop_start: bus_stop from where we start
        :param bus_stop_current: the current bus_stop
        :param bus_stop_end: bus_stop we want to go
        :param time_asked : String, time asked by the user
        :param date_asked : String, date asked by the user "regular" or we_holidays"
        :return path: list composed of the different steps
        """

        if bus_stop_current == bus_stop_end:
            return bus_stop_current.name

        # fastest_distance = {}  # distance (or time) to get to each bus_stop ex: {"bus_stop_name": {"distance":distance, "location":[bus_line_name,date, index]},...}
        # visited_bus_stop = []  # ex: [bus_stop1, bus_stop2,..]
        # predecessor = {}  # path to go to the last bus_stop and the distance to get to it ex:{"last_bus_stop":bus_stop2, "distance": minute}
        # path = []  # the fatest_path
        path.append(bus_stop_current)
        visited_bus_stop.append(bus_stop_current)

        max_time = 60*24

        for bus_stop in bus_stops:
            fastest_distance[bus_stop.name] = {"distance":  max_time,"location": []}
            # time to get to this bus stop we operate in minute
            # in case that we need more than 1 day to get to the destination, and we don't really know how does the
            # datetime object work)
        fastest_distance[bus_stop_start.name] = {"distance": 0, "location": []}
        # means that we are already at the bus stop (bus_stop_start)

        # update the new distances from
        for bus_stop_neighbour in bus_stop_current.get_bus_stop_neighbour():
            for bus_line_name in self.bus_lines_shared(bus_stop_current, bus_stop_neighbour):  # two bus stops could
                # share several bus lines
                if bus_stop_neighbour in bus_stop_current.next_bus_stop:
                    date_dir_asked = date_asked + "_go"
                else:
                    date_dir_asked = date_asked + "_back"
                index = bus_stop_current.get_index_closest_time(bus_line_name, date_dir_asked, time_asked)  # index is the index of
                # the closest time (in the bus_line_name) to time asked
                weight = self.convert_time_in_min(
                    bus_stop_current.get_time(bus_line_name, date_dir_asked, index)) - self.convert_time_in_min(
                    bus_stop_neighbour.get_time(bus_line_name, date_dir_asked, index))  # time (in minute) between these 2 bus stops


                if (predecessor["distance"] + weight) >= fastest_distance[bus_stop_neighbour.name]["distance"]:
                    fastest_distance[bus_stop_neighbour.name]["distance"] = (predecessor["distance"] + weight)
                    fastest_distance[bus_stop_neighbour.name]["location"] = [bus_line_name, date_asked, index]

        # choose the fastest unvisited bus_stop from the origin bus stop
        min_distance = max_time
        for bus_stop in bus_stops:
            if not (bus_stop in visited_bus_stop):
                if fastest_distance[bus_stop.name]["distance"] < min_distance:
                    min_bus_stop = bus_stop
                    min_distance = fastest_distance[bus_stop.name]["distance"]

        # relancer l'algorithme djikstra avec le plus court bus stop de l'origine

        return self.test_fastest(bus_stops, bus_stop_start, min_bus_stop,  bus_stop_end, time_asked, date_asked, fastest_distance, visited_bus_stop, predecessor, path)


    def dijkstra(self, bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked): # without showing the path, just take the fastest path

        # initialisation
        bus_stop_to_visit = []
        max_time = 60*24 #minute in a day
        dist = {} # ex {"bus_stop1": {"distance":dist1, "last_bus_to_get_there":{"bus_line_name":bus_line_name1, "date_dir_asked": date_dir_asked1, "index":index1}, "bus_stop2": {"distance":dist2, "last_bus_to_get_there":{"bus_line_name":bus_line_name2, "date_dir_asked": date_dir_asked2, "index":index2},...}
        # last_bus_to_get_there : the time when the bus leave the previous bus_stop to arrive to the current bus_stop
        for bus_stop in bus_stops:
            bus_stop_to_visit.append(bus_stop)
            dist[bus_stop.name] = {"distance": max_time, "last_bus_to_get_there": {"bus_line_name":None, "date_dir_asked": None, "index":None}}

        dist[bus_stop_start.name]["distance"] = 0 # set the distance from bus_stop_start to itself to 0
        dist[bus_stop_start.name]["last_bus_to_get_there"] = {"bus_line":None, "date_dir_asked": None, "index":None}
        bus_stop_to_visit.remove(bus_stop_start) # remove the bus_stop_start from bus to visit because we are already at this bus_stop
        return self.dijkstra_algorithm(bus_stops, bus_stop_start, bus_stop_end, bus_stop_start, time_asked, date_asked, bus_stop_to_visit, dist)

    def dijkstra_algorithm(self, bus_stops, bus_stop_start, bus_stop_end, bus_stop_current, time_asked, date_asked,
                          bus_stop_to_visit, dist):

        if len(bus_stop_to_visit) ==0:
            return dist

        for bus_stop_neighbour in bus_stop_current.get_bus_stop_neighbour():
            if bus_stop_neighbour in bus_stop_to_visit:

                #####
                for bus_line_name in self.bus_lines_shared(bus_stop_current, bus_stop_neighbour):  # two bus stops could
                    # share several bus lines, but we don't care if we arrive at the neighbour bus stop the fastest way
                    if bus_stop_neighbour in bus_stop_current.next_bus_stop:
                        date_dir_asked = date_asked + "_go"
                    else:
                        date_dir_asked = date_asked + "_back"
                        
                    index = bus_stop_current.get_index_closest_time(bus_line_name, date_dir_asked,
                                                                    time_asked)  # index is the index of
                    # the closest time (in the bus_line_name) to time asked

                    #time_bus_stop_current = self.convert_time_in_min(bus_stop_current.get_time(bus_line_name, date_dir_asked, index))
                    while bus_stop_neighbour.get_time(bus_line_name, date_dir_asked, index) =='-': # pour gérer la fourchette, on attend le prochain pour partir
                        index = index + 1 # even if we are in the back direction we add 1 because the schedule is reversed (kinda)

                    waiting_time = self.convert_time_in_min(bus_stop_current.schedules[bus_line_name][date_dir_asked][index]) - self.convert_time_in_min(time_asked)
                    # waiting time before taking the bus (works)

                    time_bus_stop_neighbour = self.convert_time_in_min(bus_stop_neighbour.get_time(bus_line_name, date_dir_asked, index))
                    time_bus_stop_current = self.convert_time_in_min(bus_stop_current.get_time(bus_line_name, date_dir_asked, index))

                    weight = (time_bus_stop_neighbour - time_bus_stop_current) + waiting_time # time (in minute) between these 2 bus stops

                #####
                    new_dist = weight + dist[bus_stop_current.name]["distance"]
                    if new_dist < dist[bus_stop_neighbour.name]["distance"]:
                        dist[bus_stop_neighbour.name]["distance"] = new_dist
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["bus_line_name"] = bus_line_name
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["date_dir_asked"] = date_dir_asked
                        dist[bus_stop_neighbour.name]["last_bus_to_get_there"]["index"] = index

        #choose the closest bus_stop from the initial bus_stop
        min_time = 60*24
        bus_stop_closest_to_start_and_not_yet_visited = None
        for bus_stop in bus_stop_to_visit:
            if dist[bus_stop.name]["distance"] <= min_time:
                min_time = dist[bus_stop.name]["distance"]
                bus_stop_closest_to_start_and_not_yet_visited = bus_stop

        #bus_stop_closest_to_start_and_not_yet_visited = # function
        bus_stop_to_visit.remove(bus_stop_closest_to_start_and_not_yet_visited)

        #ATTENTION : IL FAUT QUE LE TIME ASKED VARIE (IMPOSSIBLE DE TOUT LE TEMPS ARRIVER à LA MEME HEURE A UN ARRET SUR NOTRE CHEMIN
        #TIME_ASKED EST L'HEURE D'ARRIVEE AU PROCHAIN ARRET(bus_stop_closest_to_start_and_not_yet_visited),
        # pour cela je dois avoir bus_line_name, date et index

        bus_line_name1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["bus_line_name"]
        date_dir_asked1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["date_dir_asked"]
        index1 = dist[bus_stop_closest_to_start_and_not_yet_visited.name]["last_bus_to_get_there"]["index"]
        time_asked = bus_stop_closest_to_start_and_not_yet_visited.schedules[bus_line_name1][date_dir_asked1][index1]

        return self.dijkstra_algorithm(bus_stops, bus_stop_start, bus_stop_end, bus_stop_closest_to_start_and_not_yet_visited, time_asked, date_asked, bus_stop_to_visit, dist)



    def shortest(self, start_stop, end_stop):
        pass

    def fastest(self, start_stop, end_stop):
        pass

    def foremost(self, start_stop, end_stop):
        pass

    def on_same_bus_line(self, bus_stop1, bus_stop2):
        """return True if bus_stop1 and bus_stop2 are on the same bus line, else False"""
        for bus_line_name in bus_stop1.schedules:  # if they have one shared bus_line, it has to be in bus_stop1's bus lines (we could do it with bus_stop2)
            if bus_line_name in bus_stop2.schedules:
                return True
        return False

    def bus_lines_shared(self, bus_stop1, bus_stop2):
        """ return a list of all the bus line shared by two bus_stop"""
        bus_lines_shared = []  # list of names of each bus line
        for bus_line_name in bus_stop1.schedules:  # if they have one shared bus_line, it has to be in bus_stop1's bus lines (we could do it with bus_stop2)
            if bus_line_name in bus_stop2.schedules:
                bus_lines_shared.append(bus_line_name)
        return bus_lines_shared




