import json
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from itertools import groupby
import operator

ingredient_counter = {}
final = {}
cuisine_counter = {}

with open('../data/train.json') as data_file:
    data = json.load(data_file)

#pprint(data[:10])

for recipe in data:
    if recipe["cuisine"] not in cuisine_counter:
        cuisine_counter[recipe["cuisine"]] = 1
    else:
        cuisine_counter[recipe["cuisine"]] += 1

    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredient_counter:
            ingredient_counter[ingredient] = 1
        else:
            ingredient_counter[ingredient] += 1

for ingredient in ingredient_counter.keys():
    if ingredient_counter[ingredient] > 10:
        final[ingredient] = ingredient_counter[ingredient]

hi = sorted(list(ingredient_counter.values())[-100:])


xs = sorted(list(set(hi)))
ys = [len(list(group)) for key, group in groupby(hi)]

plt.plot(xs,ys)
# plt.set_yscale('log')
# plt.set_xscale('log')
plt.show()
#sorted_x = sorted(ingredient_counter.items(), key=operator.itemgetter(1))

#print(len(data))
#pprint(final)
#print(len(final))
#pprint(sorted_x)
#print(len(cuisine_counter))
#pprint(cuisine_counter)
