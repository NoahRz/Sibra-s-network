from Graph import Graph

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    #print(splitted_dates)
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

    for stop in graph.stops:
        print(stop.name, stop.schedules)
    print(len(graph.stops))

if __name__ == "__main__":
    main()