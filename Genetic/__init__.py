from abc import ABCMeta, abstractmethod, abstractproperty


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
        for mother in self.individuals:
            for father in self.individuals:
                new_generation.append(mother.breed(father, self.attributes))
        self.individuals = new_generation

    def is_stable(self):
        fitness = self.individuals[0].fitness()
        for i in self.individuals[1:]:
            if i.fitness() != fitness:
                return False
        return True

    def dump(self, file):
        with open(file, 'a') as f:
            f.write(repr(self))

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

    @abstractmethod
    def breed(self, mate):
        '''Interbreeding mechanism'''

    @abstractproperty
    def fitness():
        '''Fit - function'''
