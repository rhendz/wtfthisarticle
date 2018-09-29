import json
import re # regular expressions
import requests
from bs4 import BeautifulSoup

AUTHOR_REGEX = re.compile('author')

# Get author
def getAuthor(soupObj):
    # Returns first occurrence of matched AUTHOR_REGEX
    matched_expr = soupObj.find('', {'class' : AUTHOR_REGEX}, text=True)
    if matched_expr is not None:
        return matched_expr.get_text()
    else:
        return "No Author"

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
