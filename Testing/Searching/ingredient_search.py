import cv2
import pytesseract
import pdf2image
import os

# Given a string and a list of strings, returns a dictionary with the number of occurences
# of the 'cleaned-up' string in the list
def process_word(ingredient, words):
    dict = {}
    
    ingredient_words = ingredient.split()
    for word in ingredient_words:
        dict[word.lower().strip()] = 0

    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for word in words:
        for c in word.lower().strip():
            if c in punctuation:
                word = word.replace(c, "")
        if(word.lower().strip() in dict):
            dict[word.lower().strip()] += 1
    
    return dict

# Given two string lists, returns a dictionary with the number of occurences
# of each string from list 1 in list 2
def process_ingredients(ing_lst, words):
    dict = {}
    for ing in ing_lst:
        dict.update(process_word(ing, words))

    return dict

# Takes a string path to a pdf file as input, returns a list containing words in pdf
def pdf_to_list(path):

    # Initialize local path to tesseract
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract' # can i get around this

    # Save pages of a pdf to a series of pngs, ordered numerically
    pdf = pdf2image.convert_from_path(path)
    images = []
    for i in range(len(pdf)):
        pdf[i].save(f'cbbr_page{i+1}.png', 'PNG')
        images.append(cv2.imread(f'cbbr_page{i+1}.png'))

    # Generate a list of words that appear in the saved images
    words = []
    for img in images:
        text = pytesseract.image_to_string(img)
        words += text.split()
    
    return words

# Algorithm for rating dictionary by how well it matches the ingredients_list
# Higher return values indicate closer matches
def rate(ingredients_list, dict):
    return sum(dict.values())

# Returns a dictionary where each ingredient in the ingredients string list is mapped to the number of
# times it occurs in the recipe pdf specified by the string path
def main(ingredients_list, db_path):
    recipes = []
    for f in os.listdir(db_path):
        if os.path.isfile(os.path.join(db_path, f)):
            recipes.append(f)

    # Create a list of paths to highest matching pdfs in database to ingredients list
    best = []
    highest_rating = 0
    for recipe_path in recipes:
        dict = process_ingredients(ingredients_list, pdf_to_list(recipe_path))
        rating = rate(ingredients_list, dict)
        if rating > highest_rating:
            highest_rating = rating
            best = [recipe_path]
        elif rating > 0 and rating == highest_rating:
            best.append(recipe_path)
    
    return best
