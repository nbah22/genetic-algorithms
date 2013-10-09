from abc import ABCMeta, abstractmethod, abstractproperty
import random
import tkinter as Tk
from tkinter import filedialog


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
        self.individuals.sort(key=lambda x: -x.fitness())
        self.individuals = self.individuals[:self.size]

    def breed_all(self):
        new_generation = []
        for i in range(len(self.individuals)):
            mother = self.choose_parent()
            father = self.choose_parent()
            new_generation.append(mother.breed(father, self.attributes))
        self.individuals += new_generation

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
        self.breed_all()
        self.mutate_all()
        self.select()
        print(repr(self))

    def dump(self, file):
        with open(file, 'a') as f:
            f.write(repr(self))

    @abstractmethod
    def is_stable():
        '''Says whether population has stopped evolving'''
        return True

    @abstractmethod
    def __repr__():
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

    @abstractmethod
    def draw(self, master):
        '''Used in GUI'''


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
        Tk.Button(command=lambda: self.redraw(population.cycle),
                  text='Cycle', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(population.mutate_all),
                  text='Mutate', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(population.breed_all),
                  text='Breed', master=butframe).pack(side='left')
        Tk.Button(command=lambda: self.redraw(population.select),
                  text='Select', master=butframe).pack(side='left')
        Tk.Button(command=self.dump, text='Dump to file',
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
