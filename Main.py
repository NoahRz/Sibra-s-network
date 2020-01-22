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

    return [[regular_path, regular_date_go, regular_date_back], [we_holidays_path,we_holidays_date_go,we_holidays_date_back]]

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def main():
    data_file_name = 'data/1_Poisy-ParcDesGlaisins.txt'
    # data_file_name = 'data/2_Piscine-Patinoire_Campus.txt'

    regular_graph = Graph(data_file_name,init_network(data_file_name)[1])



if __name__ == "__Main__":
    #main()
    print(init_network('data/1_Poisy-ParcDesGlaisins.txt')[0][0])
