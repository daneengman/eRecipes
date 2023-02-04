# eRecipes

Django version 4.1.6

eRecipes is a website database of client-uploaded recipes developed in python and html. Recipes can be uploaded to the site via photo (PNG, JPEG, etc) or PDF file format.

The primary function of the website is found under the "Search" link. Here, you can search for recipes with particular ingredients to easily decide what it is you want to cook.

The core dependencies for this project are pdf2Image, OpenCV, Pytesseract, Poppler, and Django. We use pdf2Image in conjunction with poppler to convert uploaded pdfs into an image format that could then be processed by the OpenCV module. The processed images are scanned by Pytesseract for text. We then apply a series of search algorithms to find particular ingredients among the client-uploaded database of recipes and return the matching recipes to the client. The website framework and user-interface is built entirely using Django. The basis for the website comes from the LocalLibraries tutorial guide from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django . 

We modified the code from the tutorial for our website to learn the tools Django has to offer in 24 hours. 
