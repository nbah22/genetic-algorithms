import Knights


p = Knights.Population(20, x_size=5, y_size=5)
# p.individuals[0].field = [[1, 0, 1, 0, 1],
#                           [0, 1, 0, 1, 0],
#                           [1, 0, 1, 0, 1],
#                           [0, 1, 0, 1, 0],
#                           [1, 0, 1, 0, 1]]
while not p.is_stable():
    p.mutate_all()
    p.breed_all()
    p.mutate_all()
    p.select()
    print(repr(p))
    # p.dump('KnightsEvolve.txt')
p.dump('KnightsResults.txt')
