from abc import ABCMeta, abstractmethod, abstractproperty
import random
# import tkinter as Tk
# from tkinter import filedialog

import time


class Population(metaclass=ABCMeta):

    @abstractproperty
    def kind():
        '''Returns species of population'''

    def __init__(self, size, mutate_before_breeding=False, max_num_of_mutations=1, **args):
        if 'num_of_children' in args:
            self.NUM_OF_CHILDREN = args['num_of_children']
        else:
            self.NUM_OF_CHILDREN = size * 5
        self.MUTATE_BEFORE_BREEDING = mutate_before_breeding
        self.MAX_NUM_OF_MUTATIONS = max_num_of_mutations

        try:  # I agree that this is bad, but it seems to be logical
            self.individuals
        except:
            self.individuals = [self.kind(**args) for i in range(size)]

        self.attributes = args
        self.size = size

    def mutate_all(self):
        for i in range(len(self.individuals)):
            for k in range(random.randint(0, self.MAX_NUM_OF_MUTATIONS)):
                self.individuals[i].mutate()

    def select(self):
        '''Selection mechanism'''
        self.individuals.sort(key=lambda x: -x.fitness())
        self.individuals = self.individuals[:self.size]

    def breed_all(self):
        new_generation = []
        for i in range(self.NUM_OF_CHILDREN):
            mother = self.choose_parent()
            father = self.choose_parent()
            new_generation.append(mother + father)
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
        start = time.time()
        if self.MUTATE_BEFORE_BREEDING:
            self.mutate_all()
            self.breed_all()
        else:
            self.breed_all()
            self.mutate_all()
        self.select()

    def restart(self):
        del self.individuals
        self.__init__(self.size, **self.attributes)

    def dump(self, file):
        with open(file, 'a') as f:
            f.write(str(self))

    def is_stable(self):
        return all(x == self.individuals[0] for x in self.individuals[1:])

    @abstractmethod
    def __str__():
        '''Returns a visual representation of population'''
        return ''


class Species(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        '''Constructor'''

    def __add__(self, other):
        return self.breed(other)

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
        Tk.Button(command=lambda: self.redraw(self.population.restart),
                  text='Restart', master=butframe).pack(side='left')

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
