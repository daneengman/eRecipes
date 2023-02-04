import cv2
import pytesseract
import pdf2image
import json
import os

# Takes the path to a pdf and stores it to directory dir as a text file with a dictionary
def store(pdf_path, dir):
    
    # Initialize local path to tesseract
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

    # Save pages of a pdf to a series of pngs, ordered numerically
    pdf = pdf2image.convert_from_path(pdf_path)
    images = []
    for i in range(len(pdf)):
        pdf[i].save(f'cbbr_page{i+1}.png', 'PNG')
        images.append(cv2.imread(f'cbbr_page{i+1}.png'))

    # Generate a list of words that appear in the saved images
    words = []
    for img in images:
        text = pytesseract.image_to_string(img)
        words += text.split()

    d = {word:words.count(word) for word in words}

    filename = (os.path.basename(pdf_path))
    title = filename[:(len(filename)-4)]

    with open(os.path.join(dir, (title + '.txt')), 'w') as recipe_file:
        recipe_file.write(json.dumps(d))