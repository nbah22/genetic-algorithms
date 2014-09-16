import Genetic


class Population(Genetic.Population):
    def kind(self):
        return Parallelism()

    def __str__(self):
        pass


class Parallelism(Genetic.Species):
    def __eq__(self, other):
        pass

    def __init__(self):
        pass  # do something with request.py

    def breed(self, mate):
        pass

    def mutate(self):
        pass

    def draw(self, master):
        pass

    def clone(self):
        pass

    def fitness(self):
        pass