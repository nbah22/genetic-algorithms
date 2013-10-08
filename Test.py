from Knights import *


Knights = Population(10, Field, x_size=5, y_size=5)
print(repr(Knights))
Knights.mutate_all()
print(repr(Knights))
