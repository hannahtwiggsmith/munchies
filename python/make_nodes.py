import json
import pickle
from pprint import pprint
from collections import Counter

def load_data(filename):
    """Loads and pickles data if pickle file is not present."""
    try:
        data = pickle.load(open("save.pickle", "rb"))
    except FileNotFoundError:
        with open(filename) as data_file:
            data = json.load(data_file)
        pickle.dump(data, open("save.pickle", "wb"))

    return data

nodelist = []
links = []

for recipe in data:
    for ingredient in recipe["ingredients"]:
        nodelist.append(ingredient)
        for other_ingredient in recipe["ingredients"]:
            if ingredient != other_ingredient:
                links.append((ingredient,other_ingredient))

#pprint(nodelist)
#pprint(links)
#pprint(([len(list(group)) for key, group in groupby(links)])

c = Counter(elem for elem in links)
#pprint(c)

l = [(key,value) for key, value in c.items() if value > 50]
pprint(l)


if __name__ == '__main__':
    print(load_data("../data/train.json"))
