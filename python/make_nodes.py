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


def make_json(link_list, hist, path="../data/ingredients.json"):
    ingredient_struct = {"nodes":[], "links":[]}
    biggest_link = link_list[-1][1]

    ingredients = []

    with open("../data/groups.json") as data_file:
        groups = json.load(data_file)

    for group in link_list:
        if group[0][0] not in ingredients:
            ingredients.append(group[0][0])
            ingredient_struct["nodes"].append({"id": group[0][0], "group": groups[group[0][0]], "appearances":hist[group[0][0]]})
        val = (group[1]/biggest_link)*10
        #print(val)

        ingredient_struct["links"].append({"source": group[0][0], "target": group[0][1], "value": val})

    pickle.dump(ingredient_struct["links"], open("links.pickle", "wb"))

    with open(path, 'w') as outfile:
        json.dump(ingredient_struct, outfile)

    # groups = {}
    # for ingredient in ingredients:
    #     groups[ingredient] = 0
    #
    # with open("../data/groupsss.json", 'w') as outfile:
    #     json.dump(groups, outfile)


if __name__ == '__main__':
    data = load_data("../data/train.json")
    cuisine = "italian"
    nodelist, links = make_links(data, len(data), cuisine)

    c = Counter(elem for elem in links)
    appearances = Counter(elem for elem in nodelist)
    ingredient_hist = {ing[0]:ing[1] for ing in appearances.items()}


    l = [(key,value) for key, value in c.items() if value > 100]
    make_json(sorted(l,key=lambda x: x[1]), ingredient_hist)
