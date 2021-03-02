import enum
from pprint import pprint
from collections import defaultdict


class Solver:
    def __init__(self, streets, cars, D, F, I):
        self.streets = {street.name: street for street in streets}
        self.cars = set(cars)
        self.duration = D
        self.score = F
        self.nodes = [[] for i in range(I)]
        self.schedule = [[] for i in range(I)]

    def solve(self):
        self.set_route_length()
        self.set_mean_route_lengths()
        self.set_nodes()
        self.set_schedule()

    def set_route_length(self):
        for car in self.cars:
            car.route_length = 0
            for street in car.streets:
                car.route_length += self.streets[street].length

    def set_mean_route_lengths(self):
        for car in self.cars:
            for street in car.streets:
                street = self.streets[street]
                street.route_count += 1
                street.mean_route_length += car.route_length
        for street in self.streets.values():
            if street.route_count:
                street.mean_route_length /= street.route_count

    def set_nodes(self):
        for street in self.streets.values():
            self.nodes[street.end].append(street)

    def set_schedule(self):
        for idx, node in enumerate(self.nodes):
            node = sorted(filter(lambda x: x.route_count, node), key=self.sort_by_mean)

            if node:
                min_count = min(node, key=lambda x: x.route_count).route_count
                mean = sum(street.route_count for street in node) // len(node)

                for sidx, street in enumerate(node):
                    if street.route_count:
                        duration = max(1, street.route_count // (3 * min_count))
                        self.schedule[idx].append([street.name, duration])

    def sort_by_mean(self, street):
        return street.mean_route_length

    def output_res(self, filename):
        nodes_count = len(self.schedule) - self.schedule.count([])

        with open(filename, 'w') as f:
            f.write(str(nodes_count) + '\n')
            
            for idx, node in enumerate(self.schedule):

                if node:
                    f.write(str(idx) + '\n')
                    
                    street_count = len(node)
                    f.write(str(street_count) + '\n')

                    for street in node:
                        f.write(f'{street[0]} {street[1]}\n')


class Car:
    def __init__(self, idx, p: int, *streets: [str]):
        self.idx = idx
        self.p = int(p)
        self.streets = streets
        self.route_length = None

    def __str__(self):
        return 'streets :' + str(self.streets)

    def __repr__(self):
        return str(self.streets)

    def __hash__(self):
        return self.idx

    def __eq__(self, other):
        return self.idx == other.idx


class Street:
    def __init__(self, b: int, e: int, name: str, l: int):
        self.begin = int(b)
        self.end = int(e)
        self.length = int(l)
        self.name = name
        self.mean_route_length = 0
        self.route_count = 0


def read_data(filename: str):
    with open(filename) as f:
        D, I, S, V, F = [int(x) for x in f.readline().strip().split()]

        streets = [None] * S
        for i in range(S):
            streets[i] = Street(*f.readline().split())


        cars = [None] * V
        for i in range(V):
            cars[i] = Car(i, *f.readline().split())

        return D, I, S, V, F, streets, cars


if __name__ == '__main__':
    ext = '.txt'
    names =['a', 'b', 'c', 'd', 'e', 'f']

    for file in names:
        D, I, S, V, F, streets, cars = read_data('in/' + file + ext)

        s = Solver(streets, cars, D, F, I)
        s.solve()
        s.output_res('out/out_' + file + ext)