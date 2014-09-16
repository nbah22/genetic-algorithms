import Tests


if __name__ == '__main__':
    params = {'random_parents': False,
              'mother_is_good': True,
              'father_is_good': True,
              'size': 40,
              'num_of_children': 150,
              'mutate_before_breeding': False,
              'max_num_of_mutations': 8,
              'max_num_of_old_mutations': 5,
              'equal_individuals_are_allowed': False,
              'equal_parents_are_allowed': True,
              'random_individs_added_each_cycle': 20,
              'number_of_fathers': 4}
    params_range = {'size': 28,
                    'num_of_children': 120,
                    'max_num_of_mutations': 8,
                    'max_num_of_old_mutations': 5,
                    'random_individs_added_each_cycle': 20,
                    'number_of_fathers': 4}

    p = Tests.Population(size=30, params=params, params_range=params_range, log_file='log_6.txt',
                         averages_log='avg_log_6.txt', settings_file='Tests_settings.txt', load=False)
    # Genetic.GUI(p, columns=5, title='Tests')
    n = 0
    while not p.is_stable():
        p.cycle()
        n += 1
        print('\033[91m-- Cycle:\033[0m', n)
