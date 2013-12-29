from abc import ABCMeta, abstractmethod, abstractproperty
import random
import tkinter as Tk
from tkinter import filedialog
import copy
import time


class Population(metaclass=ABCMeta):

    @abstractproperty
    def kind():
        '''Returns species of population'''

    def __init__(self, **attributes):
        if 'size' not in attributes:
            attributes['size'] = 25

        # wow such code
        # many parametres
        if 'num_of_children' not in attributes:
            attributes['num_of_children'] = attributes['size'] * 5            

        if 'mutate_before_breeding' not in attributes:
            attributes['mutate_before_breeding'] = False            

        if 'max_num_of_mutations' not in attributes:
            attributes['max_num_of_mutations'] = 1

        if 'max_num_of_old_mutations' not in attributes:
            attributes['max_num_of_old_mutations'] = 0

        if 'equal_individuals_are_allowed' not in attributes:
            attributes['equal_individuals_are_allowed'] = True

        if 'random_parents' not in attributes:
            attributes['random_parents'] = False

        if 'mother_is_good' not in attributes:
            attributes['mother_is_good'] = True

        if 'father_is_good' not in attributes:
            attributes['father_is_good'] = False

        self.attributes = attributes

        # print('Population started with parametres:')
        # print(self.attributes)

        try:  # I agree that this is bad, but it seems to be logical
            self.individuals
        except:
            self.individuals = [self.kind(**attributes) for i in range(self.attributes['size'])]

    def mutate_all(self):
        if self.attributes['mutate_before_breeding']:
            for i in range(len(self.individuals)):
                for k in range(random.randint(0, self.attributes['max_num_of_mutations'])):
                    self.individuals[i].mutate()
        else:
            for i in range(len(self.individuals)):
                for k in range(random.randint(0, self.attributes['max_num_of_old_mutations'])):
                    self.individuals[i].mutate()

            for i in range(len(self.new_generation)):
                for k in range(random.randint(0, self.attributes['max_num_of_mutations'])):
                    self.new_generation[i].mutate()

            self.individuals += self.new_generation

    def select(self):
        '''Selection mechanism'''
        if not self.attributes['equal_individuals_are_allowed']:
            new_individuals = []
            for individ in self.individuals:
                if individ not in new_individuals:
                    new_individuals.append(individ)
            self.individuals = new_individuals

        self.individuals.sort(key=lambda x: -x.fitness())
        self.individuals = self.individuals[:self.attributes['size']]

    def breed_all(self):
        new_generation = []
        for i in range(self.attributes['num_of_children']):
            mother = self.choose_parent(self.attributes['mother_is_good'])
            father = self.choose_parent(self.attributes['father_is_good'])
            while father == mother:
                father = self.choose_parent(self.attributes['father_is_good'])
            new_generation.append(mother + father)
        if self.attributes['mutate_before_breeding']:
            self.individuals += new_generation
        else:
            self.new_generation = new_generation + copy.deepcopy(self.individuals)

    def choose_parent(self, good = True):
        if self.attributes['random_parents']:
            return random.choice(self.individuals)
        else:
            if good:
                fitnesses = [i.fitness() for i in self.individuals]
            else: # such constant. many bad
                fitnesses = [13 - i.fitness() for i in self.individuals]
            rnd = random.random() * sum(fitnesses)
            t = 0
            for i in range(len(fitnesses)):
                t += fitnesses[i]
                if t >= rnd:
                    return self.individuals[i]

    def cycle(self):
        start = time.time()
        if self.attributes['mutate_before_breeding']:
            self.mutate_all()
            self.breed_all()
        else:
            self.breed_all()
            self.mutate_all()
        self.select()

    def restart(self):
        del self.individuals
        self.__init__(**self.attributes)

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
        # Tk.Button(command=lambda: self.redraw(self.population.mutate_all),
        #           text='Mutate', master=butframe).pack(side='left')
        # Tk.Button(command=lambda: self.redraw(self.population.breed_all),
        #           text='Breed', master=butframe).pack(side='left')
        # Tk.Button(command=lambda: self.redraw(self.population.select),
        #           text='Select', master=butframe).pack(side='left')

        # Tk.Button(command=self.dump, text='Dump to file',
        #           master=butframe).pack(side='left')
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
