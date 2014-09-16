import tkinter as Tk
import random
import copy

import Genetic


class Population(Genetic.Population):
    def kind(self, **args):
        return Field(**args)


class Field(Genetic.Species):
    def __init__(self, population):
        self.population = population
        self.field = [[0
                       for x in range(self.population.attributes['x_size'])]
                      for y in range(self.population.attributes['y_size'])]
        for y in range(self.population.attributes['y_size']):
            self.field[y][random.randint(0, self.population.attributes['x_size'] - 1)] = 1

    def fitness(self):
        q = 0
        p = 0
        y_size = len(self.field)
        x_size = len(self.field[0])
        for y in range(y_size):
            for x in range(x_size):
                if self.field[y][x]:
                    q += 1
                    for i in range(len(self.field)):
                        if self.field[i][x] and i != y:
                            p += 1
                    else:
                        for i in range(len(self.field[0])):
                            if self.field[y][i] and i != x:
                                p += 1
                        else:
                            i = 1
                            while i + x < x_size and i + y < y_size:
                                if self.field[i + y][i + x]:
                                    p += 1
                                i += 1
                            else:
                                i = 1
                                while x - i > 0 and i + y < y_size:
                                    if self.field[i + y][x - i]:
                                        p += 1
                                    i += 1
                                else:
                                    i = 1
                                    while x - i > 0 and y - i > 0:
                                        if self.field[y - i][x - i]:
                                            p += 1
                                        i += 1
                                    else:
                                        i = 1
                                        while x + i < x_size and y - i > 0:
                                            if self.field[y - i][x + i]:
                                                p += 1
                                            i += 1
        return 2 * q - 3 * p
        # if p > 0:
        #     return k
        # else:
        #     return 0

    def mutate(self):
        a = random.randint(0, len(self.field[0]) - 1)
        b = random.randint(0, len(self.field[0]) - 1)
        tmp = self.field[a].copy()
        self.field[a] = self.field[b].copy()
        self.field[b] = tmp

    def breed(self, mates):
        child = Field(self.population)
        for y in range(len(self.field)):
            child.field[y] = random.choice([self] + mates).field[y].copy()
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
                Tk.Frame(master=frame, bg=color, width=20,
                         height=20).grid(row=y, column=x, padx=1, pady=1)
        Tk.Label(master=frame, text=self.fitness()).grid()

    def clone(self):
        clone = copy.copy(self)
        clone.field = copy.deepcopy(self.field)
        return clone

    def __eq__(self, other):
        return self.field == other.field
