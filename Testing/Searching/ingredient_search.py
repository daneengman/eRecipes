import os
import json

# extracts specified ingredient from recipe dict as a new singleton 
# dictionary
def process_word(ingredient, recipe_dict):
    dict = {}
    
    ingredient_words = ingredient.split()
    for word in ingredient_words:
        dict[word.lower().strip()] = 0

    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for word in recipe_dict:
        for c in word.lower().strip():
            if c in punctuation:
                word = word.replace(c, "")
        if(word.lower().strip() in dict):
            dict[word.lower().strip()] = recipe_dict[word]
    return dict

# create a new dictionary that extracts ingredients from the recipe_dict
def process_ingredients(ing_lst, recipe_dict):
    dict = {}
    for ingredient in ing_lst:
        dict.update(process_word(ingredient, recipe_dict))
    return dict

# Algorithm for rating dictionary by how well it matches the ingredients_list
# Higher return values indicate closer matches
def rate(ingredients_list, dict):
    return sum(dict.values())

# Takes a list of ingredients and a path to a database, returns
# a list of paths in the database that contain the recipes
# that best match the ingredients list
def main(ingredients_list, db_path):

    # recipes is a list of text files, each containing a dictionary of the words from the corresponding recipe
    recipes = []
    for f in os.listdir(db_path):
        if os.path.isfile(os.path.join(db_path, f)):
            recipes.append(f)

    best = []
    highest_rating = 0
    for recipe_path in recipes:
        # Read the dictionary from the text file
        with open(os.path.join(db_path, recipe_path)) as f:
            data = f.read()
        recipe_dict = json.loads(data)

        dict = process_ingredients(ingredients_list, recipe_dict)
        rating = rate(ingredients_list, dict)
        if rating > highest_rating:
            highest_rating = rating
            best = [recipe_path]
        elif rating > 0 and rating == highest_rating:
            best.append(recipe_path)
    
    return best
