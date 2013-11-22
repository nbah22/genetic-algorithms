from os import listdir
import re


filenames = [f for f in listdir('statistics')]
for filename in filenames:
    with open('statistics/' + filename) as f:
        txt = f.read()
    print(filename)
    num_of_tests = txt.count('Fitness: ')
    overall = [0]*13
    for i in re.findall(r'Fitness: (\d+)', txt):
        overall[- int(i)] += 1
    for i in range(len(overall)):
        if overall[i] > 0:
            print('%d: %.1f%% (%d)' % (13 - i, overall[i] / num_of_tests * 100, overall[i]))
    print('Total:', num_of_tests, '\n')
