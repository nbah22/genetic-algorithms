import Tests


if __name__ == '__main__':
    p = Tests.Population(25)
    # Genetic.GUI(p, columns=5, title='Tests')
    n = 0
    while not p.is_stable():
        p.cycle()
        n += 1
        with open('log.txt', 'a') as f:
            f.write('\n---------------Cycle: %d---------------\n' % (n))
            f.write(str(p))
        print('------ Cycle:', n, '------')
