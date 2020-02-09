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
                print("Please choose one of these : 1 Fastest path - 2 Shortest path - 3 Foremost path")
                ans3 = input()
                if int(ans3) == 1:
                    print('\n'+'\033[1;32m' + "Fastest path " + '\033[0m')
                    path = graph.dijkstra2(graph.bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked)
                    display_path(path)
                elif int(ans3) == 2:
                    print('\n'+'\033[1;32m' + "Shortest path " + '\033[0m')
                    path = graph.dijkstra3(graph.bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked)
                    display_path(path)
                elif int(ans3) == 3:
                    print('\n'+'\033[1;32m' + "Foremost path" + '\033[0m')
                    path = graph.dijkstra4(graph.bus_stops, bus_stop_start, bus_stop_end, time_asked, date_asked)
                    display_path(path)
                else:
                    print('\x1b[0;30;41m' + 'Choose one of these 3' + '\x1b[0m')
                run = False
            else:
                print('\x1b[0;30;41m' + 'this bus stop does not exist or it is same as the start one !' + '\x1b[0m')
        else:
            print('\x1b[0;30;41m' + 'this bus stop does not exist !' + '\x1b[0m')


def display(bus_stops, para=None, para1=None):
    """display the list of bus_stops
    :param bus_stops: list of bus_stops
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

def display_path(path):
    """ display the path
    :param path: list of dict of bus stop"""
    for bus_stop_dict in path:
        key = list(bus_stop_dict.keys())[0] # the first key of the dict
        if path.index(bus_stop_dict) == 0:  # the fisrt bus_stop
            print('\x1b[6;30;44m' + 'START' + '\x1b[0m')
            print("bus_stop : "+ '\033[1;34m' + key + '\033[0m' + " ,Time :", bus_stop_dict[key]["Time"])
            print("bus line :", bus_stop_dict[key]["bus_line_name"], bus_stop_dict[key]["date_dir_asked"])
            print(".\n.\n.")
        elif path.index(bus_stop_dict) == len(path)-1:  # the last bus_stop
            print("bus_stop : " + '\033[1;31m' + key + '\033[0m' + " ,Time :", bus_stop_dict[key]["Time"])
            print("bus line :", bus_stop_dict[key]["bus_line_name"], bus_stop_dict[key]["date_dir_asked"])
            print('\x1b[6;30;41m' + 'END' + '\x1b[0m')
        else:
            print("bus_stop : " + key + " ,Time :", bus_stop_dict[key]["Time"])
            print("bus line :", bus_stop_dict[key]["bus_line_name"], bus_stop_dict[key]["date_dir_asked"])
            print(".\n.\n.")


if __name__ == "__main__":
    main()
