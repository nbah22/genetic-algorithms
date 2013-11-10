import Genetic
import Knights
import random
import time
from multiprocessing import *
import tkinter as Tk


class Population(Genetic.Population):

    def __init__(self, size, load=None, **args):
        if load:
            self.individuals = []
            with open(load) as f:
                individs_params = f.read().split('\n\n')[-2:-size-2:-1]
            for i in range(size):
                params = {}
                for s in individs_params[i].split('\n'):
                    s = s.split(': ')
                    k = s[0]
                    if k in ['size', 'num_of_children', 'max_num_of_mutations']:
                        v = int(s[1])
                        params[k] = v
                    elif k == 'mutate_before_breeding':
                        params[k] = s[1] == 'True'
                self.individuals.append(Test(params=params, **args))
                print('Loaded from file:')
                print(str(self.individuals[-1]))
            print('Loading complete\n')
        super(Population, self).__init__(size, **args)

    def kind(self, **args):
        return Test(**args)

    def __str__(self):
        ret = ''
        for individ in self.individuals:
            ret += str(individ) + '\n'
        return ret


class Test(Genetic.Species):

    def __init__(self, params=None, **args):
        self.attributes = args
        self.num_of_tests = 30
        self.max_num_of_cycles = 200
        if params == None:
            self.params = {'size': random.randint(10, 50),
                           'num_of_children': random.randint(10, 200),
                           'mutate_before_breeding': random.choice([True, False]),
                           'max_num_of_mutations': random.randint(1, 10)}
        else:
            self.params = params

        self.calculate()
        print('Individual initialized\n')

    def fitness(self):
        return self.fit

    def one_test(self, i):
        start = time.time()
        p = Knights.Population(x_size=5, y_size=5, **self.params)

        n = 0
        while not p.is_stable() and n < self.max_num_of_cycles:
            p.cycle()
            n += 1

        return p.individuals[0].fitness(), n, time.time() - start

    def calculate(self):
        self.fit = 0
        self.cycles = 0
        self.timer = 0

        for k, v in self.params.items():
            print('%s: %d' % (k, v))
        pool = Pool()
        result = pool.imap(self.one_test, range(self.num_of_tests))
        pool.close()
        tmp = list(zip(*list(result)))
        max_time = max(tmp[2])
        tmp = [sum(tmp[i])/self.num_of_tests for i in range(len(tmp))]
        [self.fit, self.cycles, self.time] = tmp
        print('Fitness: %(fit).2f\nCycles: %(cycles).2f\nTime: %(time).3f' %
              {'fit': self.fit,
               'cycles': self.cycles,
               'time': self.time})
        print('Max_time: %.2f\n' % max_time)

    def mutate(self):
        key = random.choice(list(self.params.keys()))
        if key == 'mutate_before_breeding':
            self.params[key] = [True, False][int(self.params[key])]
        else:
            self.params[key] += random.randint(-3, 3)
            if self.params[key] < 1:
                self.params[key] = 1
        self.calculate()

    def breed(self, mate):
        params = self.params.copy()
        for key in params.keys():
            if key == 'mutate_before_breeding':
                params[key] = random.choice([self.params[key], mate.params[key]])
            else:
                params[key] = (self.params[key] + mate.params[key]) // 2
        child = Test(params=params, **self.attributes)
        return child

    def draw(self, master):
        frame = Tk.Frame(master=master, borderwidth=2)
        frame.pack(side='left')
        for k, v in self.params.items():
            Tk.Label(master=frame, text='%s: %s' % (k, v)).pack(side='top')
        Tk.Label(master=frame, text='Fitness: %.2f' % (self.fit)).pack(side='top')
        Tk.Label(master=frame, text='Cycles: %.2f' % (self.cycles)).pack(side='top')
        Tk.Label(master=frame, text='Time: %.2f' % (self.time)).pack(side='top')

    def __str__(self):
        output = 'Fitness: %(fit).2f\nCycles: %(cycles).2f\nTime: %(time).3f\n'
        for k, v in self.params.items():
            output += '%s: %s\n' % (k, v)
        return output % {'fit': self.fit,
                         'cycles': self.cycles,
                         'time': self.time}

    def __eq__(self, other):
        return self.params == other.params
