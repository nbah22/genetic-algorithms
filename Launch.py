import Knights
import Genetic
import profile
import pstats
import tkinter


params = {'random_parents': True,
          'mother_is_good': True,
          'father_is_good': True,
          'size': 25,
          'num_of_children': 50,
          'mutate_before_breeding': False,
          'max_num_of_mutations': 3,
          'max_num_of_old_mutations': 0,
          'equal_individuals_are_allowed': False,
          'seed': None}

#, seed='BVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVVqqqq1VVVaqqqtVVVWqqqrVVVV')
p = Knights.Population(x_size=5, y_size=5, **params)
Genetic.GUI(p, columns=5, title='Knights')

# def profile_cycle():
# 	profile.run('p.cycle()', 'Cycle')
# 	stats = pstats.Stats('Cycle')
# 	stats.sort_stats('time')
# 	stats.print_stats()

# profile.run('p = Knights.Population(x_size=5, y_size=5, **params)', 'Population_init')
# win = tkinter.Tk()
# tkinter.Button(command=profile_cycle, text='Profile one cycle').pack()
# stats = pstats.Stats('Population_init')
# stats.strip_dirs()
# stats.sort_stats('time')
# stats.print_stats()
# win.mainloop()