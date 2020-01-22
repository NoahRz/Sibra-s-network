

class Stop:

    def __init__(self, label, schedule):
        self.label = label
        self.schedule = schedule
        self.neighbour = []

    def add_neighbour(self, neighbour):
        """ add the next bus stop"""
        self.neighbour.append(neighbour)

