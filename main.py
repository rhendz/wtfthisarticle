from bs4 import BeautifulSoup
from googlesearch import search
from newspaper import Article
import datetime
import json
import nltk
import re
import requests

## nltk.download('punkt')

# Custom scripts
from modules.summarize import *
from modules.sentiment import *

## Useful for extracting author if newspaper fails
AUTHOR_REGEX = re.compile('(author)|(byline)', re.I) # Ignore case

article_data = {
    'title': -1,
    'author': -1,
    'publish_date': -1,
    'img_src': -1,
    'text': -1
}

# This fnc has a much higher success rate at finding the author
def getAuthor(article):
    # Must turn article into a soup obj
    soupObj = BeautifulSoup(article.html, 'html.parser')

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
        return -1

    # Find firstmost child
    while matched_expr.findChild() is not None:
        matched_expr = matched_expr.findChild()

    if matched_expr is not None:
        return re.sub(r'By ', '', matched_expr.get_text())
    else:
        return -1

def getInitJSON(Url):
    ## BEGIN BUILDING INITIAL ARTICLE
    article = Article(Url.strip()) # Instantiate article
    article.download() # Required
    article.parse() # Required

    title = article.title
    # for counter, _ in enumerate (title[::-1]):
    #     if (title[counter] == '-'):
    #         title = title[:counter]
    #         break

    author_head = article.authors ## Sometimes this fnc. does not work
    if len(author_head) == 0:
        author_head = getAuthor(article) # Try again w my fnc
    else:
        author_head = article.authors[0]

    publish_date = article.publish_date
    img_src = article.top_image
    summary = article.summary
    text = article.text
    summary = summarize(text)

    try:
        article_data['title'] = title
        article_data['author'] = author_head
        # datetime objs are not serializable
        article_data['publish_date'] = publish_date.strftime("%Y-%m-%d")
        article_data['img_src'] = img_src
        article_data['text'] = text
    except AttributeError:
        pass # This is fine
    ## END BUILDING INITIAL ARTICLE

    with open('modules/json/init.json', 'w') as outfile:
        json.dump(article_data, outfile)

    if text is not None or text != '':
        summarize(text)

    num_page = 2
    search_results = google.search(title, num_page)
    for result in search_results:
        with open('modules/json/relatedLinks.json', 'w') as outfile:
            json.dump(result.link, outfile)

    # Sentiment analysis
    analyze(text);


getInitJSON(input("Enter a Url: \n"))
