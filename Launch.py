import Knights
import Genetic


p = Knights.Population(25, x_size=5, y_size=5)
# Genetic.GUI(p, columns=5, title='Knights')
print(p.individuals[0].field)
print(p.individuals[0].b64())
print(p.b64decode(p.individuals[0].b64()).field)
seed = p.get_seed()
print(seed)
print(len(seed))
# while not p.is_stable():
#     p.cycle()
# print(str(p))
