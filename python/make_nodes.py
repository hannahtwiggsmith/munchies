import json
import operator
import pickle
from pprint import pprint
from collections import Counter


def load_data(filename="../data/train.json"):
    """Loads and pickles data if pickle file is not present."""
    try:
        data = pickle.load(open("save.pickle", "rb"))
    except FileNotFoundError:
        with open(filename) as data_file:
            data = json.load(data_file)
        pickle.dump(data, open("save.pickle", "wb"))

    return data


def make_links(data, num_recipes, cuisine):
    nodelist = []
    links = []

    for recipe in data[:num_recipes]:
        if recipe["cuisine"] == cuisine:
            for ingredient in recipe["ingredients"]:
                nodelist.append(ingredient)
                for other_ingredient in recipe["ingredients"]:
                    if ingredient != other_ingredient:
                        links.append((ingredient,other_ingredient))

    return (nodelist, links)


def make_json(link_list, path="../data/ingredients.json"):
    ingredient_struct = {"nodes":[], "links":[]}

    ingredients = []

    for group in link_list:
        if group[0][0] not in ingredients:
            ingredients.append(group[0][0])
            ingredient_struct["nodes"].append({"id": group[0][0], "group": 0})

        ingredient_struct["links"].append({"source": group[0][0], "target": group[0][1], "value": group[1]})

    with open(path, 'w') as outfile:
        json.dump(ingredient_struct, outfile)


if __name__ == '__main__':
    data = load_data("../data/train.json")
    cuisine = "italian"
    nodelist, links = make_links(data, len(data), cuisine)

    c = Counter(elem for elem in links)

    l = [(key,value) for key, value in c.items() if value > 50]
    make_json(l)
    # pprint(sorted(l,key=lambda x: x[1]))
    #pprint(nodelist)
    #pprint(links)
    #pprint(([len(list(group)) for key, group in groupby(links)])
