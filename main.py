import json
import re # regular expressions
import requests
from bs4 import BeautifulSoup

AUTHOR_REGEX = re.compile('.author.')

# Get author
def getAuthor(soupObj):
    # Returns first occurrence of matched AUTHOR_REGEX
    for elem in soupObj.findAll('', {'class' : AUTHOR_REGEX}, text=True):
        if elem is not None: return elem.get_text()

def getInitJSON(Url):
    r = requests.get(Url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    print(getAuthor(soup))

    # # Get title
    # title = soup.title.get_text()
    # print(title)
    #
    # # Get author
    # author = getAuthor(soup)
    #
    # # Get header image
    # imageSrc = soup.img.get("src")
    # print(imageSrc)
    # # Get text
    # print(soup.get_text())
    #
    # # Get author name
    #
    # initJSON = {
    #     'title': title,
    #     'author': author,
    #     'imageHeader': imageSrc,
    #     'text':
    # }

getInitJSON(input("Enter a Url: \n"))
