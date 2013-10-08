import sys
sys.path.append("..")
import Genetic
import random


class Population(Genetic.Population):
    def breed():
        pass

    def __repr__(self):
        ret = ''
        for y in range(self.attributes['y_size']):
            ret += '| '
            for i in range(self.size):
                ret += ' '.join([str(i) for i in self.individuals[i].field[y]])
                ret += ' | '
            ret += '\n'
        return ret


class Field(Genetic.Species):
    def __init__(self, args):
        self.field = [[random.randint(0, 1)
                      for x in range(args['x_size'])]
                      for y in range(args['y_size'])]

    def fitness():
        return 0

    def mutate(self):
        x = random.randint(0, len(self.field) - 1)
        y = random.randint(0, len(self.field[0]) - 1)
        if self.field[x][y]:
            self.field[x][y] = 0
        else:
            self.field[x][y] = 1
