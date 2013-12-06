import Genetic
import Knights
import random
import time
import re
from multiprocessing import *
import tkinter as Tk


class Population(Genetic.Population):

    def __init__(self, size, log_file, settings_file, load=False, mutate_before_breeding=False, max_num_of_mutations=1, **args):
        if 'num_of_children' in args:
            self.NUM_OF_CHILDREN = args['num_of_children']
        else:
            self.NUM_OF_CHILDREN = size * 5
        self.MUTATE_BEFORE_BREEDING = mutate_before_breeding
        self.MAX_NUM_OF_MUTATIONS = max_num_of_mutations
        self.attributes = args
        self.size = size
        self.log = log_file
        self.settings = settings_file

        if load:
            with open(self.log) as f:
                log = f.read()
            breeding_pos = log.rfind('Breeding')
            mutation_pos = log.rfind('Mutation')
            new_cycle_pos = log.rfind('New cycle')
            last = max(breeding_pos, mutation_pos, new_cycle_pos)

            if last == new_cycle_pos:
                individs_params = log.split('\n---------------New cycle---------------\n')[-1].split('\n\n')[:-1]
                if len(individs_params) == size:
                    self.individuals = self.load_individs(individs_params, settings=self.settings, log=self.log, **args)
                else:
                    raise Exception("Wrong size")

            elif last == breeding_pos:
                print('loading from breeding')
                nextgen_params = log.split('Breeding:\n')[-1].split('\n\n')[:-1]
                individs_params = log.split('Breeding:\n')[-2].split('\n\n')[-size - 2:-1]
                print('Individuals:')
                self.individuals = self.load_individs(individs_params, settings=self.settings, log=self.log, **args)
                print('Nextgen:')
                nextgen = self.load_individs(nextgen_params, settings=self.settings, log=self.log, **args)
                print('Loading complete\n')
                self.breed_all(new_generation=nextgen)
                with open(self.log, 'a') as f:
                    f.write('Mutation:\n')
                self.mutate_all()
                self.select()
                with open(self.log, 'a') as f:
                    f.write('\n---------------New cycle---------------\n')
                    f.write(str(self))

            elif last == mutation_pos:
                log2 = log
                log = log[:mutation_pos]
                print('loading from mutation')
                nextgen_params = log.split('Breeding:\n')[-1].split('\n\n')[:-1]
                individs_params = log.split('Breeding:\n')[-2].split('\n\n')[-size - 2:-1]
                mutated_params = log2.split('Mutation:\n')[-1].split('\n\n')[:-1]
                print('Individuals:')
                self.individuals = self.load_individs(individs_params + nextgen_params + mutated_params, settings=self.settings, log=self.log, **args)
                print('Loading complete\n')
                self.select()
                with open(self.log, 'a') as f:
                    f.write('\n---------------New cycle---------------\n')
                    f.write(str(self))
        else:
            self.individuals = [self.kind(settings=self.settings, **args) for i in range(size)]

    def load_individs(self, individs_params, **args):
        individuals = []
        for i in range(len(individs_params)):
            params = {}
            for s in individs_params[i].split('\n'):
                s = s.split(': ')
                k = s[0]
                if k in ['size', 'num_of_children', 'max_num_of_mutations']:
                    v = int(s[1])
                    params[k] = v
                elif k == 'mutate_before_breeding':
                    params[k] = (s[1] == 'True')
                elif k == 'Fitness':
                    fit = float(s[1])
                elif k == 'Cycles':
                    cycles = float(s[1])
                elif k == 'Time':
                    t = float(s[1])
            individuals.append(Test(test=False, params=params, **args))
            individuals[-1].fit = fit
            individuals[-1].cycles = cycles
            individuals[-1].timer = t
            print('Loaded from file:')
            print(str(individuals[-1]))
        return individuals

    def cycle(self):
        start = time.time()
        if self.MUTATE_BEFORE_BREEDING:
            with open(self.log, 'a') as f:
                f.write('Mutation:\n')
            self.mutate_all()
            with open(self.log, 'a') as f:
                f.write('Breeding:\n')
            self.breed_all()
        else:
            with open(self.log, 'a') as f:
                f.write('Breeding:\n')
            self.breed_all()
            with open(self.log, 'a') as f:
                f.write('Mutation:\n')
            self.mutate_all()
        self.select()
        with open(self.log, 'a') as f:
            f.write('\n---------------New cycle---------------\n')
            f.write(str(self))
        return time.time() - start

    def breed_all(self, new_generation=None):
        if new_generation is None:
            new_generation = []
        for i in range(len(new_generation), self.NUM_OF_CHILDREN):
            mother = self.choose_parent()
            father = self.choose_parent()
            new_generation.append(mother + father)
        print('NEW_GENERATION_SIZE ==', len(new_generation))
        self.individuals += new_generation
        print('INDIVIDUALS:', len(self.individuals))

    def kind(self, **args):
        return Test(**args)

    def __str__(self):
        ret = ''
        for individ in self.individuals:
            ret += str(individ) + '\n'
        return ret


class Test(Genetic.Species):

    def __init__(self, test=True, params=None, **args):
        self.attributes = args
        self.num_of_tests = 50
        self.max_num_of_cycles = 500
        if params == None:
            self.params = {'size': random.randint(10, 50),
                           'num_of_children': random.randint(10, 200),
                           'mutate_before_breeding': random.choice([True, False]),
                           'max_num_of_mutations': random.randint(1, 10)}
        else:
            self.params = params
        if test:
            self.calculate()

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
        with open(self.attributes['settings']) as f:
            t = re.search(r'Pools: (.+)', f.read()).group(1)
            try:
                num_of_pools = int(t)
            except:
                if time.localtime()[3] < 7:
                    num_of_pools = 1
                else:
                    num_of_pools = None
        pool = Pool(num_of_pools)
        result = pool.imap(self.one_test, range(self.num_of_tests))
        pool.close()
        tmp = list(zip(*list(result)))
        max_time = max(tmp[2])
        tmp = [sum(tmp[i]) / self.num_of_tests for i in range(len(tmp))]
        [self.fit, self.cycles, self.timer] = tmp
        with open(self.attributes['log'], 'a') as f:
            f.write(str(self))
            f.write('Max_time: %.2f\n\n' % max_time)

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
                params[key] = random.choice(
                    [self.params[key], mate.params[key]])
            else:
                params[key] = (self.params[key] + mate.params[key]) // 2
        child = Test(params=params, **self.attributes)
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
                 (self.time)).pack(side='top')

    def __str__(self):
        output = 'Fitness: %(fit).4f\nCycles: %(cycles).4f\nTime: %(time).4f\n'
        for k, v in self.params.items():
            output += '%s: %s\n' % (k, v)
        return output % {'fit': self.fit,
                         'cycles': self.cycles,
                         'time': self.timer}

    def __eq__(self, other):
        return self.params == other.params
