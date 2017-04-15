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
    if ingredient_counter[ingredient] > :
        final[ingredient] = ingredient_counter[ingredient]

hi = sorted(list(ingredient_counter.values())[-100:])


xs = sorted(list(set(hi)))
ys = [len(list(group)) for key, group in groupby(hi)]

print(len(cuisine_counter))
pprint(cuisine_counter)
