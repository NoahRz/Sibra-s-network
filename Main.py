from Graph import Graph


def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    # print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic


def main():
    data_file_name1 = '1_Poisy-ParcDesGlaisins.txt'
    data_file_name2 = '2_Piscine-Patinoire_Campus.txt'

    graph = Graph()
    graph.add_bus_line(data_file_name1)
    graph.add_bus_line(data_file_name2)

    # for bus_stop in graph.bus_stops: # display test
    #     l = ["prev:"]
    #     for b in bus_stop.prev_bus_stop:
    #         l.append(b.name)
    #     l.append("next:")
    #     for b in bus_stop.next_bus_stop:
    #         l.append(b.name)
    #     print(bus_stop.name, l)

    # for stop in graph.bus_stops: # display test
    #     print(stop.name, stop.schedules)
    # print(len(graph.bus_stops))

    run = True
    size = len(graph.bus_stops)
    while run:
        print("START :")
        # we enter the bus stop's number in case that the user doesn't know how to write the bus stop name
        display(graph.bus_stops)
        print("Select a number :")
        # print("a")
        ans = input()
        if 0 <= int(ans) < size:
            print("END :")
            # print again the list of bus stop with the start selected
            display(graph.bus_stops, para=ans)
            bus_stop_start = graph.bus_stops[int(ans)]
            print("Select a number:")
            ans1 = input()
            if 0 <= int(ans1) < size and ans1 != ans:
                # print again the list of bus stop with the start and the end selected
                display(graph.bus_stops, para=ans, para1=ans1)
                bus_stop_end = graph.bus_stops[int(ans1)]
                print("Departure time ? (hour:min) :")
                time_asked = input()
                print("0-regular_date or 1-we_holidays_date ?")
                ans2 = input()
                if int(ans2) == 0:
                    date_asked = "regular"
                else:
                    date_asked = "we_holidays"
                # path = graph.find_path_new(bus_stop_start, bus_stop_end)

                dist2 = graph.dijkstra2(graph.bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked)
                print(dist2)
                # path_names = []
                # # path = graph.find_path(bus_stop_start, bus_stop_end, time_asked, date_asked)
                # for bus_stop in path:
                #     path_names.append(bus_stop.name)
                # print(path_names)
                # #print(path)
                run = False
            else:
                print('\x1b[0;30;41m' + 'this bus stop does not exist or it is same as the start one !' + '\x1b[0m')
        else:
            print('\x1b[0;30;41m' + 'this bus stop does not exist !' + '\x1b[0m')


def display(bus_stops, para=None, para1=None):
    """display the list of bus_stops
    :param bus_stops: list og bus_stops
    :param para: int, answer of the user
    :param para1: int, answer of the user
    """
    i = 0
    for bus_stop in bus_stops:
        if i != 0 and (i % 5) == 0:  # print 5 elements per line
            print()
        if (para is not None) and int(para) == bus_stops.index(bus_stop):
            print('\033[1;34m' + '{0:<25s}'.format(str(
                bus_stops.index(bus_stop)) + " " + bus_stop.name) + '\033[0m', end=' ')  # display, blue text color
        elif (para1 is not None) and int(para1) == bus_stops.index(bus_stop):
            print('\033[1;31m' + '{0:<25s}'.format(str(
                bus_stops.index(bus_stop)) + " " + bus_stop.name) + '\033[0m', end=' ')  # display, red text color
        else:
            print('{0:<25s}'.format(str(bus_stops.index(bus_stop)) + " " + bus_stop.name), end=' ')
        i = i + 1
    print()  # to stop printing on the same line


if __name__ == "__main__":
    main()
