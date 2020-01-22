from Bus_line import Bus_line
from Graph import Graph

def init_network(data_file_name):
    try:
        with open(data_file_name, 'r') as f:
            content = f.read()
    except OSError:
        # 'File not found' error message.
        print("File not found")

    slited_content = content.split("\n\n")
    regular_path = slited_content[0]
    regular_date_go = dates2dic(slited_content[1])
    regular_date_back = dates2dic(slited_content[2])
    we_holidays_path = slited_content[3]
    we_holidays_date_go = dates2dic(slited_content[4])
    we_holidays_date_back = dates2dic(slited_content[5])

    return {"regular":[regular_path, regular_date_go, regular_date_back], "holidays": [we_holidays_path, we_holidays_date_go, we_holidays_date_back]}

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    #print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def main():
    data_file_name = '1_Poisy-ParcDesGlaisins.txt'
    # # data_file_name = '2_Piscine-Patinoire_Campus.txt'

    bus_1_name = data_file_name[:len(data_file_name)-4]
    bus_1 = Bus_line(bus_1_name)
    bus_1.init_stop_regular(init_network(data_file_name)["regular"][1], init_network(data_file_name)["regular"][2])

    bus_1.init_stop_holidays(init_network(data_file_name)["holidays"][1], init_network(data_file_name)["holidays"][2])

    for stop in bus_1.regular_stops:
        print(stop.name,"\n schedule_go : ", stop.schedule_go , "\n schedule_back :", stop.schedule_back)

if __name__ == "__main__":
    main()
    #print("init ", init_network('1_Poisy-ParcDesGlaisins.txt')["regular"][1])
