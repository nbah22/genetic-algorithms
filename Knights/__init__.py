import sys
sys.path.append("..")
import Genetic
import tkinter as Tk
import random


class Population(Genetic.Population):
    def kind(self, args):
        return Field(args)

    def is_stable(self):
        individ = self.individuals[0]
        for i in self.individuals[1:]:
            if i.field != individ.field:
                return False
        return True

    def __repr__(self):
        ret = ''
        for y in range(self.attributes['y_size']):
            ret += '| '
            for i in range(len(self.individuals)):
                ret += ' '.join([str(i) for i in self.individuals[i].field[y]])
                ret += ' | '
            ret += '\n'
        for i in self.individuals:
            num = str(i.fitness())
            width = self.attributes['x_size']
            ret += ' ' * (width + 1 - len(num)) + num + ' ' * (width + 1)
        ret += '\n'
        return ret


class Field(Genetic.Species):
    def __init__(self, args):
        self.field = [[random.randint(0, 1)
                      for x in range(args['x_size'])]
                      for y in range(args['y_size'])]

    def fitness(self):
        k = 0
        p = 0
        y_size = len(self.field)
        x_size = len(self.field[0])
        for y in range(y_size):
            for x in range(x_size):
                if self.field[y][x]:
                    k += 1
                    if y >= 2 and x >= 1 and self.field[y-2][x-1]:
                        p += 1
                    if y >= 2 and x < x_size-1 and self.field[y-2][x+1]:
                        p += 1
                    if y < y_size-2 and x >= 1 and self.field[y+2][x-1]:
                        p += 1
                    if y < y_size-2 and x < x_size-1 and self.field[y+2][x+1]:
                        p += 1

                    if y >= 1 and x >= 2 and self.field[y-1][x-2]:
                        p += 1
                    if y >= 1 and x < x_size-2 and self.field[y-1][x+2]:
                        p += 1
                    if y < y_size-1 and x >= 2 and self.field[y+1][x-2]:
                        p += 1
                    if y < y_size-1 and x < x_size-2 and self.field[y+1][x+2]:
                        p += 1
        p = p // 2
        return k - p*2

    def mutate(self):
        for i in range(random.randint(0, 7)):
            y = random.randint(0, len(self.field) - 1)
            x = random.randint(0, len(self.field[0]) - 1)
            if self.field[y][x]:
                self.field[y][x] = 0
            else:
                self.field[y][x] = 1

    def breed(self, mate, attributes):
        child = Field(attributes)
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                if random.randint(0, 1):
                    child.field[y][x] = mate.field[y][x]
                else:
                    child.field[y][x] = self.field[y][x]
        return child

    def draw(self, master):
        frame = Tk.Frame(master=master, borderwidth=2)
        frame.pack(side='left')
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                if self.field[y][x]:
                    color = 'black'
                else:
                    color = 'grey'
                Tk.Frame(master=frame, bg=color, padx=1, pady=1,
                         width=20, height=20).grid(row=y, column=x)
