from abc import ABCMeta, abstractmethod, abstractproperty
import random
import tkinter as Tk
from tkinter import filedialog


class Population(metaclass=ABCMeta):

    @abstractproperty
    def kind(self):
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

        try:  # I agree that this is bad, but it seems to be logical
            self.individuals
        except:
            self.individuals = [self.kind(population=self) for i in range(self.attributes['size'])]

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
            if not self.attributes['equal_parents_are_allowed']:
                while father == mother:
                    father = self.choose_parent(self.attributes['father_is_good'])
            new_generation.append(mother + father)
        if self.attributes['mutate_before_breeding']:
            self.individuals += new_generation
        else:
            self.new_generation = new_generation + [individ.clone() for individ in self.individuals]

    def choose_parent(self, good=True):
        if self.attributes['random_parents']:
            return random.choice(self.individuals)
        else:
            if good:
                fitnesses = [i.fitness() for i in self.individuals]
            else:  # such constant. many bad
                fitnesses = [13 - i.fitness() for i in self.individuals]
            rnd = random.random() * sum(fitnesses)
            t = 0
            for i in range(len(fitnesses)):
                t += fitnesses[i]
                if t >= rnd:
                    return self.individuals[i]

    def cycle(self):
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
        for x in self.individuals[1:]:
            if x != self.individuals[0]:
                return False
        else:
            return True

    @abstractmethod
    def __str__(self):
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
    def clone(self):
        '''A method which returns a copy of an object'''

    @abstractmethod
    def __eq__(self, other):
        '''Says whether two individuals are equal'''
        return True


class GUI():

    def __init__(self, population, columns, title=None):
        self.columns = columns
        self.population = population
        self.win = Tk.Tk()
        self.win.resizable(0, 0)
        if title:
            self.win.title("Genetic: %s" % (title))
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
        Tk.Button(command=lambda: self.show_settings_window(),
                  text='Settings', master=butframe).pack(side='left')

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

    def change_parameter(self, param, value=None):
        if value is None:
            value = False if self.population.attributes[param] else True
        self.population.attributes[param] = value
        self.tk_vars[param].set(self.population.attributes[param])

    def make_scale(self, param, label, from_, to):
        self.tk_vars[param] = Tk.IntVar()
        self.tk_vars[param].set(self.population.attributes[param])
        s = Tk.Scale(command=lambda x: self.change_parameter(param, int(x)),
                     from_=from_, to=to, master=self.settings_window,
                     orient='horizontal', label=label,
                     variable=self.tk_vars[param])
        s.pack(anchor="w")

    def make_checkbutton(self, param, label):
        self.tk_vars[param] = Tk.IntVar()
        self.tk_vars[param].set(self.population.attributes[param])
        Tk.Checkbutton(command=lambda: self.change_parameter(param),
                       master=self.settings_window, text=label,
                       variable=self.tk_vars[param]).pack(anchor="w")

    def load_preset(self, preset):
        self.population.attributes.update(preset)
        for key in self.tk_vars:
            self.tk_vars[key].set(self.population.attributes[key])

    def show_settings_window(self):
        try:
            self.settings_window.focus()
        except:
            self.settings_window = Tk.Toplevel()
            self.settings_window.resizable(0, 0)
            self.settings_window.title('Genetic: Settings')
            self.tk_vars = {}

            self.make_scale('size', 'Size:', 1, 40)
            self.make_scale('num_of_children', 'Children:', 0, 1000)
            self.make_scale('max_num_of_mutations', 'Mutations:', 0, 25)
            self.make_scale('max_num_of_old_mutations', 'Old mutations:', 0, 25)
            self.make_checkbutton('random_parents', 'Parents are random')
            self.make_checkbutton('mutate_before_breeding', 'Mutate before breeding')
            self.make_checkbutton('equal_individuals_are_allowed', 'Equal individuals are allowed')
            self.make_checkbutton('equal_parents_are_allowed', 'Equal parents are allowed')
            Tk.Label(master=self.settings_window, text="Presets:").pack()

            # Presets
            good = {'random_parents': False,
                    'mother_is_good': True,
                    'father_is_good': True,
                    'size': 25,
                    'num_of_children': 1000,
                    'mutate_before_breeding': False,
                    'max_num_of_mutations': 10,
                    'max_num_of_old_mutations': 0,
                    'equal_individuals_are_allowed': True,
                    'equal_parents_are_allowed': True}

            default = {'random_parents': True,
                       'mother_is_good': True,
                       'father_is_good': True,
                       'size': 25,
                       'num_of_children': 300,
                       'mutate_before_breeding': False,
                       'max_num_of_mutations': 5,
                       'max_num_of_old_mutations': 0,
                       'equal_individuals_are_allowed': False,
                       'equal_parents_are_allowed': True}

            long_lasting = {'random_parents': False,
                            'mother_is_good': True,
                            'father_is_good': True,
                            'size': 25,
                            'num_of_children': 20,
                            'mutate_before_breeding': False,
                            'max_num_of_mutations': 3,
                            'max_num_of_old_mutations': 0,
                            'equal_individuals_are_allowed': False,
                            'equal_parents_are_allowed': False}

            Tk.Button(master=self.settings_window, text="Good but slow",
                      command=lambda: self.load_preset(good)).pack(side="left")
            Tk.Button(master=self.settings_window, text="Default",
                      command=lambda: self.load_preset(default)).pack(side="left")
            Tk.Button(master=self.settings_window, text="Long-lasting",
                      command=lambda: self.load_preset(long_lasting)).pack(side="left")

            geom_arr = self.win.geometry().split('+')
            size_x, size_y = geom_arr[0].split('x')
            self.settings_window.geometry('+%d+%d' % (int(size_x) + int(geom_arr[1]) + 5, int(geom_arr[2])))

            self.settings_window.mainloop()
