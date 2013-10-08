from abc import ABCMeta, abstractmethod, abstractproperty


class Population(metaclass=ABCMeta):
    def __init__(self, size, kind, **args):
        self.individuals = [kind(args) for i in range(size)]
        self.attributes = args
        self.size = size

    def mutate_all(self):
        for i in range(self.size):
            self.individuals[i].mutate()

    def select(self):
        '''Selection mechanism'''
        self.individuals.sort(key=lambda x: -x.fitness())
        self.individuals = self.individuals[:self.size]

    @abstractmethod
    def breed():
        '''Interbreeding mechanism'''

    @abstractmethod
    def __repr__():
        '''Print a visual representation of population to console'''


class Species(metaclass=ABCMeta):
    @abstractmethod
    def __init__():
        '''Constructor'''

    @abstractmethod
    def mutate():
        '''Mutation mechanism'''

    @abstractproperty
    def fitness():
        '''Fit - function'''
