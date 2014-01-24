import Knights
import Genetic


# You can change some parameters and see what happens
# This can be done in graphical interface as well
params = {'random_parents': True,
          'mother_is_good': True,
          'father_is_good': True,
          'size': 25,
          'num_of_children': 300,
          'mutate_before_breeding': False,
          'max_num_of_mutations': 5,  # The larger are fields - the more mutations you will need
          'max_num_of_old_mutations': 0,  # Number of mutations of old generation
          'equal_individuals_are_allowed': False,
          'equal_parents_are_allowed': True,
          'seed': None}  # Seed is a parameter which no one should use. Ever.
                         # But you can try setting it to "BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV"

p = Knights.Population(x_size=5, y_size=5, **params)  # You can try using x_size=8 and y_size=8 instead, then
Genetic.GUI(p, columns=5, title='Knights')            # it is better to make max_num_of_mutations=7 or more
