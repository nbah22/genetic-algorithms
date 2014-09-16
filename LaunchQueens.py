import Queens
import Genetic


# You can change some parameters and see what happens
# This can be done in graphical interface as well
params = {'random_parents': False,
          'size': 45,
          'num_of_children': 200,
          'max_num_of_mutations': 0,  # The larger are fields - the more mutations you will need
          'max_num_of_old_mutations': 2,  # Number of mutations of old generation
          'equal_individuals_are_allowed': False,
          'equal_parents_are_allowed': False,
          'random_individs_added_each_cycle': 20,
          'number_of_fathers': 3,
          'seed': None}  # Seed is a parameter which no one should use. Ever.
# But you can try setting it to "BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV"

p = Queens.Population(x_size=8, y_size=8, **params)  # You can try using x_size=8 and y_size=8 instead, then
Genetic.GUI(p, columns=5, title='Queens')  # it is better to make max_num_of_mutations=7 or more
