import json
import operator
import pickle
from collections import Counter
from pprint import pprint


def load_data(filename="../data/train.json"):
  """Loads and pickles data if pickle file is not present."""
  # try:
  #   data = pickle.load(open("save.pickle", "rb"))
  # except FileNotFoundError:
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
            links.append((ingredient, other_ingredient))

  return (nodelist, links)


def make_groups(ingredients):
  groups = {}
  for ingredient in ingredients:
    groups[ingredient[0][0]] = 0

  with open("../data/groups_" + cuisine + ".json", 'w') as outfile:
    json.dump(groups, outfile)


def make_json(link_list, hist):
  ingredient_struct = {"nodes": [], "links": []}
  biggest_link = link_list[-1][1]

  ingredients = []

  with open("../data/groups_" + cuisine + "_final.json") as data_file:
    groups = json.load(data_file)

  for group in link_list:
    if group[0][0] not in ingredients:
      ingredients.append(group[0][0])
      ingredient_struct["nodes"].append(
          {"id": group[0][0],
           "group": groups[group[0][0]],
           "appearances": hist[group[0][0]]})
    val = (group[1] / biggest_link) * 10

    ingredient_struct["links"].append(
        {"source": group[0][0], "target": group[0][1], "value": val})

  pickle.dump(ingredient_struct["links"], open("links.pickle", "wb"))

  with open("../data/ingredients_" + cuisine + ".json", 'w') as outfile:
    json.dump(ingredient_struct, outfile)


if __name__ == '__main__':
  data = load_data("../data/train.json")
  cuisine = "italian"
  nodelist, links = make_links(data, len(data), cuisine)

  c = Counter(elem for elem in links)
  appearances = Counter(elem for elem in nodelist)
  ingredient_hist = {ing[0]: ing[1] for ing in appearances.items()}

  l = [(key, value) for key, value in c.items()]
  l_sorted = sorted(l, key=lambda x: x[1])[-250:]

  # pprint(sorted(l, key=lambda x: x[1]))
  # make_groups(l)
  make_json(l_sorted, ingredient_hist)
