import sys
if sys.version_info[0] < 3:
    print('Your interpreter has version %d.%d.%d.' % (sys.version_info[:3]))
    print('Please use Python 3 interpreter as this program does not support backwards compatibility.')
    sys.exit()

import Knights
import Genetic


# You can change some parameters and see what happens
# This can be done in graphical interface as well
params = {'random_parents': False,
          'size': 40,
          'num_of_children': 300,
          'max_num_of_mutations': 1,  # The larger are fields - the more mutations you will need
          'max_num_of_old_mutations': 7,  # Number of mutations of old generation
          'equal_individuals_are_allowed': False,
          'equal_parents_are_allowed': False,
          'random_individs_added_each_cycle': 20,
          'number_of_fathers': 0,
          'seed': None}  # Seed is a parameter which no one should use. Ever.
                         # But you can try setting it to "BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV"

p = Knights.Population(x_size=5, y_size=5, **params)  # You can try using x_size=8 and y_size=8 instead, then
# it is better to make max_num_of_mutations=7 or more
Genetic.GUI(p, columns=5, title='Knights')
