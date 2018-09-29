from newspaper import Article
import datetime
import json

def getInitJSON(Url):
    ## BEGIN BUILDING INITIAL ARTICLE
    article_data = {}
    article = Article(Url) # Instantiate article
    article.download() # Required
    article.parse() # Required

    title = article.title
    author_head = article.authors[0] # This does not correctly parse all the time
    publish_date = article.publish_date;
    img_src = article.top_image;
    text = article.text;

    article_data['title'] = title
    article_data['author'] = author_head
    # datetime objs are not serializable
    article_data['publish_date'] = publish_date.strftime("%Y-%m-%d")
    article_data['img_src'] = img_src
    article_data['text'] = text
    ## END BUILDING INITIAL ARTICLE
    
    with open('json/init.json', 'w') as outfile:
        json.dump(article_data, outfile)

getInitJSON(input("Enter a Url: \n"))
