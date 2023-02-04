import cv2
import pytesseract
import pdf2image
import os

#Define path to tessaract.exe
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

prefix = 'eRecipes/Testing/Recipes/'

# List of each folder containing different recipe types
recipes_types = os.listdir(prefix)

for type_path in [prefix + type for type in recipes_types]:

    # List of individual recipe pdfs
    recipes = os.listdir(type_path)

    for recipe_path in [type_path + '/' + recipe for recipe in recipes]:

        # Convert path into a pdf
        pdf = pdf2image.convert_from_path(recipe_path)

        # Create list of images from each page of the pdf
        images = []
        for i in range(len(pdf)):
            pdf[i].save(f'cbbr_page{i+1}.png', 'PNG')
            images.append(cv2.imread(f'cbbr_page{i+1}.png'))

        # Convert each image into text
        for img in images:
            text = pytesseract.image_to_string(img)
            print(text)