import Tests


if __name__ == '__main__':
	params = {'random_parents': False,
	          'mother_is_good': True,
	          'father_is_good': True,
	          'size': 25,
	          'num_of_children': 150,
	          'mutate_before_breeding': False,
	          'max_num_of_mutations': 5,
	          'max_num_of_old_mutations': 5,
	          'equal_individuals_are_allowed': False,
	          'equal_parents_are_allowed': True}
	params_range = {'size': 15,
	                'num_of_children': 120,
	                'max_num_of_mutations': 5,
	                'max_num_of_old_mutations': 5}

	p = Tests.Population(size=25, params=params, params_range=params_range, log_file='log3.txt', settings_file='Tests_settings.txt', load=False)
	# Genetic.GUI(p, columns=5, title='Tests')
	n = 0
	while not p.is_stable():
		p.cycle()
		n += 1
		print('--------------------Cycle:', n)
