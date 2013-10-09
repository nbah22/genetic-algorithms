import Knights
import Genetic


p = Knights.Population(16, x_size=5, y_size=5)
Genetic.GUI(p, columns=4, title='Knights')
