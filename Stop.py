

class Stop:

    def __init__(self, name, schedule_go = [], schedule_back = []):
        self.name = name
        self.schedule_go = schedule_go
        self.schedule_back = schedule_back
        self.neighbour = []



    def add_neighbour(self, neighbour):
        """ add the next bus stop"""
        self.neighbour.append(neighbour)

