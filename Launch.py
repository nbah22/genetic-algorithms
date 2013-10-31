import Knights
import Genetic


p = Knights.Population(25, x_size=5, y_size=5)#, seed='BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV')
Genetic.GUI(p, columns=5, title='Knights')
seed = p.get_seed()
print(seed)
print(len(seed))
