from abc import ABCMeta, abstractmethod, abstractproperty
import random
import tkinter as Tk
from tkinter import filedialog

import time


class Population(metaclass=ABCMeta):
    @abstractproperty
    def kind():
        '''Represents species of population'''

    def __init__(self, size, **args):
        self.individuals = [self.kind(args) for i in range(size)]
        self.attributes = args
        self.size = size

    def mutate_all(self):
        for i in range(self.size):
            self.individuals[i].mutate()

    def select(self):
        '''Selection mechanism'''
        lst = []
        for individ in self.individuals:
            if individ not in lst:
                lst.append(individ)
        # likenesses = [sum(a.likeness(b) for b in lst) for a in lst]
        # i = 0
        # while i < len(lst):
        #     if likenesses[i] > sum(likenesses) / len(lst):
        #         del lst[i]
        #         del likenesses[i]
        #     else:
        #         i += 1
        self.individuals = sorted(lst, key=lambda x: -x.fitness())[:self.size]

    def breed_all(self):
        new_generation = []

        # for i in range(len(self.individuals)):
        #     mother = self.choose_parent()
        #     father = self.choose_parent()
        #     new_generation.append(mother.breed(father, self.attributes))
        for mother in self.individuals:
            for father in self.individuals:
                new_generation.append(mother.breed(father, self.attributes))

        self.individuals = new_generation

    def choose_parent(self):
        fitnesses = [i.fitness() for i in self.individuals]
        min_fitness = min(fitnesses)
        fitnesses = list(map(lambda x: x - min_fitness + 1, fitnesses))
        overall_fitness = sum(fitnesses)
        rnd = random.random()
        t = 0
        for i in range(len(self.individuals)):
            t += fitnesses[i] / overall_fitness
            if t >= rnd:
                return self.individuals[i]

    def cycle(self):
        start = time.time()
        self.breed_all()
        self.mutate_all()
        self.select()
        print(str(self), 'Cycle time: ', time.time() - start)

    def dump(self, file):
        with open(file, 'a') as f:
            f.write(str(self))

    # def is_stable():
    #     return all(x == self.individuals[0] for x in self.individuals)

    @abstractmethod
    def __str__():
        '''Returns a visual representation of population'''
        return ''


class Species(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        '''Constructor'''

    @abstractmethod
    def mutate(self):
        '''Mutation mechanism'''

    @abstractmethod
    def breed(self, mate):
        '''Interbreeding mechanism'''

    @abstractproperty
    def fitness(self):
        '''Fit - function'''

    @abstractproperty
    def likeness(self, other):
        '''Return the coefficient of likeness of two individuals'''
        return 0

    @abstractmethod
    def draw(self, master):
        '''Used in GUI'''

    @abstractmethod
    def __eq__(self, other):
        '''Says whether two individuals are equal'''
        return True


class GUI():
    def __init__(self, population, columns, title=None):
        self.columns = columns
        self.population = population
        self.win = Tk.Tk()
        if title:
            self.win.title("Genetic: " + title)
        else:
            self.win.title("Genetic")

        butframe = Tk.Frame()
        Tk.Button(command=lambda: self.redraw(self.population.cycle),
                  text='Cycle', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(self.population.mutate_all),
                  text='Mutate', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(self.population.breed_all),
                  text='Breed', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(self.population.select),
                  text='Select', master=butframe).pack(side='left')

        Tk.Button(command=self.dump, text='Dump to file',
                  master=butframe).pack(side='left')
        Tk.Button(command=self.restart, text='Restart',
                  master=butframe).pack(side='left')

        butframe.pack()
        self.popframe = None
        self.redraw()
        self.win.mainloop()

    def redraw(self, function=None):
        if function:
            function()
        if self.popframe:
            self.popframe.destroy()

        self.popframe = Tk.Frame()
        self.popframe.pack()
        if self.columns:
            for i in range(len(self.population.individuals)):
                if i % self.columns == 0:
                    row = Tk.Frame(master=self.popframe)
                    row.pack(side='top')
                self.population.individuals[i].draw(row)
        else:
            for individ in self.population.individuals:
                individ.draw(self.popframe)

    def dump(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            self.population.dump(filename)

    def restart(self):
        self.population = self.population.__class__(self.population.size, **self.population.attributes)
        self.redraw()
