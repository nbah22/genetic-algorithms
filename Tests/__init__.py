import random
import time
import copy
import re
from multiprocessing import *
import tkinter as Tk

import Genetic
import Knights


class Population(Genetic.Population):
    # def __init__(self, size, log_file, settings_file, load=False, tests_params, **args):
    #     if 'num_of_children' in args:
    #         self.NUM_OF_CHILDREN = args['num_of_children']
    #     else:
    #         self.NUM_OF_CHILDREN = size * 5
    #     self.MUTATE_BEFORE_BREEDING = mutate_before_breeding
    #     self.MAX_NUM_OF_MUTATIONS = max_num_of_mutations
    #     self.attributes = args
    #     self.size = size
    #     self.log = log_file
    #     self.settings = settings_file

    #     # if load:
    #     #     with open(self.log) as f:
    #     #         log = f.read()
    #     #     breeding_pos = log.rfind('Breeding')
    #     #     mutation_pos = log.rfind('Mutation')
    #     #     new_cycle_pos = log.rfind('New cycle')
    #     #     last = max(breeding_pos, mutation_pos, new_cycle_pos)

    #     #     if last == new_cycle_pos:
    #     #         individs_params = log.split('\n---------------New cycle---------------\n')[-1].split('\n\n')[:-1]
    #     #         if len(individs_params) == size:
    #     #             self.individuals = self.load_individs(individs_params, settings=self.settings, log=self.log, **args)
    #     #         else:
    #     #             raise Exception("Wrong size")

    #     #     elif last == breeding_pos:
    #     #         print('loading from breeding')
    #     #         nextgen_params = log.split('Breeding:\n')[-1].split('\n\n')[:-1]
    #     #         individs_params = log.split('Breeding:\n')[-2].split('\n\n')[-size - 2:-1]
    #     #         print('Individuals:')
    #     #         self.individuals = self.load_individs(individs_params, settings=self.settings, log=self.log, **args)
    #     #         print('Nextgen:')
    #     #         nextgen = self.load_individs(nextgen_params, settings=self.settings, log=self.log, **args)
    #     #         print('Loading complete\n')
    #     #         self.breed_all(new_generation=nextgen)
    #     #         with open(self.log, 'a') as f:
    #     #             f.write('Mutation:\n')
    #     #         self.mutate_all()
    #     #         self.select()
    #     #         with open(self.log, 'a') as f:
    #     #             f.write('\n---------------New cycle---------------\n')
    #     #             f.write(str(self))

    #     #     elif last == mutation_pos:
    #     #         log2 = log
    #     #         log = log[:mutation_pos]
    #     #         print('loading from mutation')
    #     #         nextgen_params = log.split('Breeding:\n')[-1].split('\n\n')[:-1]
    #     #         individs_params = log.split('Breeding:\n')[-2].split('\n\n')[-size - 2:-1]
    #     #         mutated_params = log2.split('Mutation:\n')[-1].split('\n\n')[:-1]
    #     #         print('Individuals:')
    #     #         self.individuals = self.load_individs(individs_params + nextgen_params + mutated_params, settings=self.settings, log=self.log, **args)
    #     #         print('Loading complete\n')
    #     #         self.select()
    #     #         with open(self.log, 'a') as f:
    #     #             f.write('\n---------------New cycle---------------\n')
    #     #             f.write(str(self))
    #     # else:
    #     #     self.individuals = [self.kind(settings=self.settings, **args) for i in range(size)]

    # def load_individs(self, individs_params, **args):
    #     individuals = []
    #     for i in range(len(individs_params)):
    #         params = {}
    #         for s in individs_params[i].split('\n'):
    #             s = s.split(': ')
    #             k = s[0]
    #             if k in ['size', 'num_of_children', 'max_num_of_mutations']:
    #                 v = int(s[1])
    #                 params[k] = v
    #             elif k == 'mutate_before_breeding':
    #                 params[k] = (s[1] == 'True')
    #             elif k == 'Fitness':
    #                 fit = float(s[1])
    #             elif k == 'Cycles':
    #                 cycles = float(s[1])
    #             elif k == 'Time':
    #                 t = float(s[1])
    #         individuals.append(Test(test=False, params=params, **args))
    #         individuals[-1].fit = fit
    #         individuals[-1].cycles = cycles
    #         individuals[-1].timer = t
    #         print('Loaded from file:')
    #         print(str(individuals[-1]))
    #     return individuals

    # def cycle(self):
    #     start = time.time()
    #     if self.MUTATE_BEFORE_BREEDING:
    #         with open(self.log, 'a') as f:
    #             f.write('Mutation:\n')
    #         self.mutate_all()
    #         with open(self.log, 'a') as f:
    #             f.write('Breeding:\n')
    #         self.breed_all()
    #     else:
    #         with open(self.log, 'a') as f:
    #             f.write('Breeding:\n')
    #         self.breed_all()
    #         with open(self.log, 'a') as f:
    #             f.write('Mutation:\n')
    #         self.mutate_all()
    #     self.select()
    #     with open(self.log, 'a') as f:
    #         f.write('\n---------------New cycle---------------\n')
    #         f.write(str(self))
    #     return time.time() - start

    # def breed_all(self, new_generation=None):
    #     if new_generation is None:
    #         new_generation = []
    #     for i in range(len(new_generation), self.NUM_OF_CHILDREN):
    #         mother = self.choose_parent()
    #         father = self.choose_parent()
    #         new_generation.append(mother + father)
    #     print('NEW_GENERATION_SIZE ==', len(new_generation))
    #     self.individuals += new_generation
    #     print('INDIVIDUALS:', len(self.individuals))

    def __init__(self, **args):
        self.current_cycle = 1
        super().__init__(**args)

    def kind(self, **args):
        return Test(**args)

    def __str__(self):
        ret = ''
        for individ in self.individuals:
            ret += str(individ) + '\n'
        return ret

    def cycle(self):
        with open(self.attributes['averages_log'], 'a') as f:
            f.write('\n-- Cycle: %d\n' % self.current_cycle)
        self.current_cycle += 1
        super().cycle()


class Test(Genetic.Species):
    def __init__(self, population, params=None, loaded=False):
        self.population = population
        if params is None:
            params = population.attributes['params']
            params_range = population.attributes['params_range']
        else:
            params_range = None
        self.log_file = population.attributes['log_file']
        self.averages_log = population.attributes['averages_log']
        self.settings_file = population.attributes['settings_file']
        self.num_of_tests = 25
        self.max_num_of_cycles = 50
        self.max_time = 15
        if params_range is None:
            self.params = params
        else:
            print('Random params')
            self.params = {}
            for k, v in params.items():
                if type(v) == bool:
                    self.params[k] = random.choice([True, False])
                elif type(v) == int:
                    self.params[k] = params[k] + random.randint(-params_range[k], params_range[k])
                else:
                    print('\033[91m-- Wrong type of parameter %s = %s: %s\033[0m' % (k, v, type(v)))
            print()
        print('Loaded =', loaded)
        if loaded is False:
            with open(self.log_file, 'a') as f:
                f.write('New individual:\n')
                print('New individual:')

    def one_test(self, _):
        try:
            start = time.time()
            p = Knights.Population(x_size=5, y_size=5, **self.params)

            n = 0
            if self.params['equal_individuals_are_allowed']:
                while not p.is_stable() and time.time() - start < self.max_time and n < self.max_num_of_cycles:
                    p.cycle()
                    n += 1
            else:
                while time.time() - start < self.max_time and n < self.max_num_of_cycles:
                    p.cycle()
                    n += 1

            with open('current_test.txt', 'a') as f:
                print('Fitness: %d\nCycles: %d\nTime: %.3f\n' % (p.individuals[0].fitness(), n, time.time() - start))
                f.write(
                    'Fitness: %d\nCycles: %d\nTime: %.3f\n\n' % (p.individuals[0].fitness(), n, time.time() - start))
            return p.individuals[0].fitness(), n, time.time() - start
        except:
            return 0, 0, 0

    def fitness(self):
        self.fit = 0
        self.cycles = 0
        self.timer = 0

        with open(self.log_file, 'a') as f:
            for k, v in self.params.items():
                f.write('%s: %s\n' % (k, v))
                print('%s: %s' % (k, v))
            f.write('\n')
            print()

        try:
            with open(self.settings_file) as f:
                t = re.search(r'Pools: (.+)', f.read()).group(1)
                num_of_pools = int(t)
                print('\033[91m-- Number of pools: %d\033[0m' % num_of_pools)
        except:
            print('\033[91m-- Failed to read the number of pools setting\033[0m')
            if time.localtime()[3] < 7:
                num_of_pools = 1
            else:
                num_of_pools = None

        f = open('current_test.txt', 'w')
        f.close()
        pool = Pool(num_of_pools)
        result = pool.imap(self.one_test, range(self.num_of_tests))
        pool.close()
        tmp = list(zip(*list(result)))
        max_time = max(tmp[2])
        tmp = [sum(tmp[i]) / self.num_of_tests for i in range(len(tmp))]
        [self.fit, self.cycles, self.timer] = tmp
        with open(self.log_file, 'a') as f:
            f.write('Average:\nFitness: %.2f\nCycles: %.2f\nTime: %.4f\n\n' % (self.fit, self.cycles, self.timer))
            print('Average:\nFitness: %.2f\nCycles: %.2f\nTime: %.4f\n' % (self.fit, self.cycles, self.timer))
        with open(self.averages_log, 'a') as f:
            f.write('%s\n' % self.fit)
        return self.fit

    def mutate(self):
        with open(self.log_file, 'a') as f:
            f.write('Mutation:\nOld params:\n')
            print('Mutation:\nOld params:')
            for k, v in self.params.items():
                f.write('%s: %s\n' % (k, v))
                print('%s: %s' % (k, v))
        key = random.choice(list(self.params.keys()))
        if type(self.params[key]) == bool:
            self.params[key] = [True, False][int(self.params[key])]  # Swapping true and false
        else:
            r = self.population.attributes['params_range'][key] // 4  # random value
            self.params[key] += random.randint(-r, r)
            if self.params[key] <= 0:
                if key == 'size':
                    self.params[key] = 1
                else:
                    self.params[key] = 0
        with open(self.log_file, 'a') as f:
            f.write('\nNew params:\n')
            print('\nNew params:\n')

    def breed(self, mates):
        with open(self.log_file, 'a') as f:
            f.write('Breeding:\n')
            print('Breeding:')
            f.write('Mother\'s params:\n')
            print('Mother\'s params:')
            for k, v in self.params.items():
                f.write('%s: %s\n' % (k, v))
                print('%s: %s' % (k, v))
            f.write('\nFather\'s params:\n')
            print('\nFather\'s params:')
            for k, v in mates[0].params.items():
                f.write('%s: %s\n' % (k, v))
                print('%s: %s' % (k, v))
            f.write('\n')
            print()

        params = self.params.copy()
        for key in params.keys():
            if type(self.params[key]) == bool:
                params[key] = random.choice(
                    [self.params[key], mates[0].params[key]])
            else:
                # a = bin(self.params[key])[2:]
                # b = bin(mate.params[key])[2:]
                # if len(a) > len(b):
                #     b = '0'*(len(a) - len(b)) + b
                # else:
                #     a = '0'*(len(b) - len(a)) + a
                # params[key] = int(''.join([random.choice([a[i], b[i]]) for i in range(len(a))]), 2)
                params[key] = (self.params[key] + mates[0].params[key]) // 2
        child = Test(self.population, params=params)
        return child

    def draw(self, master):
        frame = Tk.Frame(master=master, borderwidth=2)
        frame.pack(side='left')
        for k, v in self.params.items():
            Tk.Label(master=frame, text='%s: %s' % (k, v)).pack(side='top')
        Tk.Label(master=frame, text='Fitness: %.2f' %
                                    (self.fit)).pack(side='top')
        Tk.Label(master=frame, text='Cycles: %.2f' %
                                    (self.cycles)).pack(side='top')
        Tk.Label(master=frame, text='Time: %.2f' %
                                    (self.timer)).pack(side='top')

    def __str__(self):
        output = 'Fitness: %(fit).4f\nCycles: %(cycles).4f\nTime: %(time).4f\n'
        for k, v in self.params.items():
            output += '%s: %s\n' % (k, v)
        return output % {'fit': self.fit,
                         'cycles': self.cycles,
                         'time': self.timer}

    def __eq__(self, other):
        return self.params == other.params

    def clone(self):
        clone = copy.copy(self)
        clone.params = copy.deepcopy(self.params)
        return clone
