import sys
sys.path.append("..")
import Genetic
import random


class Population(Genetic.Population):
    def breed(mother, father):
        pass

    def __repr__(self):
        ret = ''
        for y in range(self.attributes['y_size']):
            ret += '| '
            for i in range(self.size):
                ret += ' '.join([str(i) for i in self.individuals[i].field[y]])
                ret += ' | '
            ret += '\n'
        # for i in self.individuals:
        #     width = self.attributes['x_size']
        #         ret += ' ' * width + str(i.fitness()) + ' ' * width
        return ret


class Field(Genetic.Species):
    def __init__(self, args):
        self.field = [[random.randint(0, 1)
                      for x in range(args['x_size'])]
                      for y in range(args['y_size'])]

    def fitness(self):
        f = 0
        x_size = len(self.field[0])
        y_size = len(self.field)
        for x in range(x_size):
            for y in range(y_size):
                if self.field[y][x]:
                    f += 1
                    if y >= 2 and x >= 1 and self.field[y-2][x-1]:
                        f -= 1
                    if y >= 2 and x < x_size-1 and self.field[y-2][x+1]:
                        f -= 1
                    if y < y_size-2 and x >= 1 and self.field[y+2][x-1]:
                        f -= 1
                    if y < y_size-2 and x < x_size-1 and self.field[y+2][x+1]:
                        f -= 1

                    if y >= 1 and x >= 2 and self.field[y-1][x-2]:
                        f -= 1
                    if y >= 1 and x < x_size-2 and self.field[y-1][x+2]:
                        f -= 1
                    if y < y_size-1 and x >= 2 and self.field[y+1][x-2]:
                        f -= 1
                    if y < y_size-1 and x < x_size-2 and self.field[y+1][x+2]:
                        f -= 1
        return f

    def mutate(self):
        x = random.randint(0, len(self.field) - 1)
        y = random.randint(0, len(self.field[0]) - 1)
        if self.field[x][y]:
            self.field[x][y] = 0
        else:
            self.field[x][y] = 1
