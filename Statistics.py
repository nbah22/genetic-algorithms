import Knights
import time


num_of_tests = 500

params = {'max_num_of_cycles': 300,
          'random_parents': False,
          'mother_is_good': True,
          'father_is_good': True,
          'size': 25,
          'num_of_children': 20,
          'mutate_before_breeding': False,
          'max_num_of_mutations': 3,
          'max_num_of_old_mutations': 0,
          'equal_individuals_are_allowed': False,
          'equal_parents_are_allowed': False,
          'seed': None}

filename = '%(max_num_of_cycles)d_%(random_parents)d_%(mother_is_good)d_%(father_is_good)d_%(size)d_%(num_of_children)d_%(mutate_before_breeding)d_%(max_num_of_mutations)d_%(seed)s_%(equal_individuals_are_allowed)d_%(max_num_of_old_mutations)d.txt' % params
f = open('statistics/' + filename, 'a+')
if f.tell() == 0:
    for k, v in params.items():
        f.write('%(key)s: %(value)s\n' % {'key': k, 'value': v})
    f.write('\n')
f.close()

output = '\n%(initial_seed_or_blank)s%(individ)s\n Fitness: %(fit)d\n Cycles: %(cycles)d\n Time: %(time).3f\n'

for i in range(num_of_tests):
    start = time.time()
    p = Knights.Population(x_size=5, y_size=5, **params)
    initial_seed = (p.get_seed() + '\n' if params['seed'] is None else '')

    n = 0
    while not p.is_stable() and n < params['max_num_of_cycles']:
        p.cycle()
        n += 1

    with open('statistics/' + filename, 'a+') as f:
        f.write(output % {'initial_seed_or_blank': initial_seed,
                          'individ': str(p.individuals[0]),
                          'fit': p.individuals[0].fitness(),
                          'cycles': n,
                          'time': time.time() - start})
    print('%.1f%%' % (i / num_of_tests * 100))
print('%.1f%%' % (100))
