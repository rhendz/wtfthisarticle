import json
import re # regular expressions
import requests
from bs4 import BeautifulSoup

AUTHOR_REGEX = re.compile('(author)|(byline)', re.I) # Ignore case

# Get author
# Still kind of spotty - does not grab all authors,
# For example, https://www.nytimes.com/2018/09/28/us/politics/brett-kavanaugh-fact-check.html?action=click&module=Spotlight&pgtype=Homepage
def getAuthor(soupObj):
    # Returns first occurrence of matched AUTHOR_REGEX
    matched_expr = soupObj.find('', {'class' : AUTHOR_REGEX})

    # Try itemprop
    if matched_expr is None:
        matched_expr = soupObj.find('', {'itemprop' : AUTHOR_REGEX})

    # Try href
    if matched_expr is None:
        matched_expr = soupObj.find('', {'href' : re.compile('profile', re.I)})

    # Nothing left to check, returns
    if matched_expr is None:
        return "No Author Found"

    # Find firstmost child
    while matched_expr.findChild() is not None:
        matched_expr = matched_expr.findChild()

    if matched_expr is not None:
        return re.sub(r'By ', '', matched_expr.get_text())
    else:
        return "No Author Found"

def getInitJSON(Url):
    r = requests.get(Url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    author = getAuthor(soup)

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
