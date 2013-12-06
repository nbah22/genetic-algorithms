import Knights
import Genetic


params = {'size': 30,
          # 'num_of_children': None,
          # 'mutate_before_breeding': None,
          'max_num_of_mutations': 2,
          'max_num_of_old_mutations': 1,
          'equal_individuals_are_allowed': False}

p = Knights.Population(x_size=5, y_size=5, **params)#, seed='BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV')
Genetic.GUI(p, columns=5, title='Knights')
seed = p.get_seed()
print(seed)
print(len(seed))
