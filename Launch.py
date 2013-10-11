import Knights
import Genetic


p = Knights.Population(25, x_size=5, y_size=5)
Genetic.GUI(p, columns=5, title='Knights')
# while not p.is_stable():
#     p.cycle()
# print(str(p))
