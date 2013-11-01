import Genetic
import Knights
import random
import time
import tkinter as Tk


class Population(Genetic.Population):

    def kind(self, **args):
        return Test(**args)

    def __str__(self):
        ret = ''
        for individ in self.individuals:
            ret += str(individ) + '\n'
        return ret


class Test(Genetic.Species):

    def __init__(self, **args):
        self.attributes = args
        num_of_tests = 1
        max_num_of_cycles = 50
        self.params = {'size': random.randint(10, 50),
                       'num_of_children': random.randint(10, 200),
                       'mutate_before_breed': random.choice([True, False]),
                       'max_num_of_mutations': random.randint(1, 10)}

        fit = 0
        cycles = 0
        timer = 0

        for k, v in self.params.items():
            print('%s: %d' % (k, v))

        for i in range(num_of_tests):
            start = time.time()
            p = Knights.Population(x_size=5, y_size=5, **self.params)

            n = 0
            while not p.is_stable() and n < max_num_of_cycles:
                p.cycle()
                n += 1

            fit += p.individuals[0].fitness()
            cycles += n
            timer += time.time() - start
            print('Test (%d/%d) completed in %.2f (%d cycles)' % (i + 1, num_of_tests, time.time() - start, n))

        self.fit = fit / num_of_tests
        self.cycles = cycles / num_of_tests
        self.time = timer / num_of_tests
        print('Individual initialized\n')


    def fitness(self):
        return self.fit / self.cycles

    def mutate(self):
        key = random.choice(list(self.params.keys()))
        if key == 'mutate_before_breed':
            self.params[key] = [True, False][int(self.params[key])]
        else:
            self.params[key] += random.randint(-5, 5)

    def breed(self, mate):
        child = Test(**self.attributes)
        for key in self.params.keys():
            if key == 'mutate_before_breed':
                child.params[key] = random.choice([self.params[key], mate.params[key]])
            else:
                child.params[key] = (self.params[key] + mate.params[key]) / 2
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
        output = 'Fitness: %(fit)d\n Cycles: %(cycles)d\n Time: %(time).3f\n'
        return output % {'fit': self.fit,
                         'cycles': self.cycles,
                         'time': self.time}

    def __eq__(self, other):
        return self.params == self.params
