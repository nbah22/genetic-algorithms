import Tests


if __name__ == '__main__':
    p = Tests.Population(25, 'log2.txt', 'Tests_settings.txt', load=True)
    # Genetic.GUI(p, columns=5, title='Tests')
    n = 0
    while not p.is_stable():
        p.cycle()
        n += 1
        print('--------------------Cycle:', n)
